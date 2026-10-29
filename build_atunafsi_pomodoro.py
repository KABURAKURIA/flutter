import os
import subprocess
import shutil

def run_cmd(cmd, cwd=None):
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, cwd=cwd, check=True)

def build_app():
    app_name = "atunafsi_pomodoro"
    if os.path.exists(app_name):
        shutil.rmtree(app_name)

    # 1. Create Flutter app
    run_cmd(["flutter", "create", "--platforms=android", "--org", "com.atunafsi", app_name])

    app_dir = os.path.abspath(app_name)

    # Remove default test directory
    test_dir = os.path.join(app_dir, "test")
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

    # 2. Add dependencies
    deps = ["provider", "sqflite", "path", "path_provider", "shared_preferences", "lottie"]
    run_cmd(["flutter", "pub", "add"] + deps, cwd=app_dir)

    # 3. Setup assets
    assets_dir = os.path.join(app_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)

    shutil.copy("./atunafsi.jpg", os.path.join(assets_dir, "atunafsi.jpg"))

    # create minimal lottie animation
    lottie_json = r"""{"v":"5.5.2","fr":29.9700012207031,"ip":0,"op":60.0000024438501,"w":500,"h":500,"nm":"Circle Animation","ddd":0,"assets":[],"layers":[{"ddd":0,"ind":1,"ty":4,"nm":"Shape Layer 1","sr":1,"ks":{"o":{"a":0,"k":100,"ix":11},"r":{"a":0,"k":0,"ix":10},"p":{"a":0,"k":[250,250,0],"ix":2},"a":{"a":0,"k":[0,0,0],"ix":1},"s":{"a":1,"k":[{"i":{"x":[0.833,0.833,0.833],"y":[0.833,0.833,0.833]},"o":{"x":[0.167,0.167,0.167],"y":[0.167,0.167,0.167]},"t":0,"s":[0,0,100]},{"i":{"x":[0.833,0.833,0.833],"y":[0.833,0.833,0.833]},"o":{"x":[0.167,0.167,0.167],"y":[0.167,0.167,0.167]},"t":30.000001221925,"s":[100,100,100]},{"t":60.0000024438501,"s":[0,0,100]}],"ix":6}},"ao":0,"shapes":[{"ty":"gr","it":[{"d":1,"ty":"el","s":{"a":0,"k":[200,200],"ix":2},"p":{"a":0,"k":[0,0],"ix":3},"nm":"Ellipse Path 1","mn":"ADBE Vector Shape - Ellipse","hd":false},{"ty":"fl","c":{"a":0,"k":[0.898039215686,0.38431372549,0.301960784314,1],"ix":4},"o":{"a":0,"k":100,"ix":5},"r":1,"bm":0,"nm":"Fill 1","mn":"ADBE Vector Graphic - Fill","hd":false},{"ty":"tr","p":{"a":0,"k":[0,0],"ix":2},"a":{"a":0,"k":[0,0],"ix":1},"s":{"a":0,"k":[100,100],"ix":3},"r":{"a":0,"k":0,"ix":6},"o":{"a":0,"k":100,"ix":7},"sk":{"a":0,"k":0,"ix":4},"sa":{"a":0,"k":0,"ix":5},"nm":"Transform"}],"nm":"Ellipse 1","np":3,"cix":2,"bm":0,"ix":1,"mn":"ADBE Vector Group","hd":false}],"ip":0,"op":60.0000024438501,"st":0,"bm":0}]}"""
    with open(os.path.join(assets_dir, "animation.json"), "w") as f:
        f.write(lottie_json)

    # Update pubspec.yaml to include assets
    pubspec_path = os.path.join(app_dir, "pubspec.yaml")
    with open(pubspec_path, "a") as f:
        f.write("\n  assets:\n    - assets/\n")

    # 4. Write Dart code
    lib_dir = os.path.join(app_dir, "lib")

    # models/task.dart
    os.makedirs(os.path.join(lib_dir, "models"), exist_ok=True)
    with open(os.path.join(lib_dir, "models", "task.dart"), "w") as f:
        f.write(r"""
class Task {
  int? id;
  String title;
  bool isCompleted;
  int pomodorosSpent;

  Task({this.id, required this.title, this.isCompleted = false, this.pomodorosSpent = 0});

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'title': title,
      'isCompleted': isCompleted ? 1 : 0,
      'pomodorosSpent': pomodorosSpent,
    };
  }

  factory Task.fromMap(Map<String, dynamic> map) {
    return Task(
      id: map['id'],
      title: map['title'],
      isCompleted: map['isCompleted'] == 1,
      pomodorosSpent: map['pomodorosSpent'],
    );
  }
}
""")

    # db/database_helper.dart
    os.makedirs(os.path.join(lib_dir, "db"), exist_ok=True)
    with open(os.path.join(lib_dir, "db", "database_helper.dart"), "w") as f:
        f.write(r"""
import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';
import '../models/task.dart';

class DatabaseHelper {
  static final DatabaseHelper instance = DatabaseHelper._init();
  static Database? _database;

  DatabaseHelper._init();

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDB('pomodoro.db');
    return _database!;
  }

  Future<Database> _initDB(String filePath) async {
    final dbPath = await getDatabasesPath();
    final path = join(dbPath, filePath);

    return await openDatabase(path, version: 1, onCreate: _createDB);
  }

  Future _createDB(Database db, int version) async {
    await db.execute('''
CREATE TABLE tasks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  isCompleted INTEGER NOT NULL,
  pomodorosSpent INTEGER NOT NULL
)
''');
  }

  Future<Task> create(Task task) async {
    final db = await instance.database;
    final id = await db.insert('tasks', task.toMap());
    task.id = id;
    return task;
  }

  Future<List<Task>> readAllTasks() async {
    final db = await instance.database;
    final maps = await db.query('tasks', orderBy: 'id DESC');
    return maps.map((json) => Task.fromMap(json)).toList();
  }

  Future<int> update(Task task) async {
    final db = await instance.database;
    return db.update('tasks', task.toMap(), where: 'id = ?', whereArgs: [task.id]);
  }

  Future<int> delete(int id) async {
    final db = await instance.database;
    return await db.delete('tasks', where: 'id = ?', whereArgs: [id]);
  }
}
""")

    # providers/pomodoro_provider.dart
    os.makedirs(os.path.join(lib_dir, "providers"), exist_ok=True)
    with open(os.path.join(lib_dir, "providers", "pomodoro_provider.dart"), "w") as f:
        f.write(r"""
import 'package:flutter/material.dart';
import 'dart:async';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/task.dart';
import '../db/database_helper.dart';

enum TimerMode { pomodoro, shortBreak, longBreak }

class PomodoroProvider with ChangeNotifier {
  TimerMode _mode = TimerMode.pomodoro;
  int _workDuration = 25;
  int _shortBreakDuration = 5;
  int _longBreakDuration = 15;

  int _timeLeft = 25 * 60;
  bool _isRunning = false;
  Timer? _timer;

  List<Task> _tasks = [];
  int _totalPomodoros = 0;

  PomodoroProvider() {
    _loadSettings();
    _loadTasks();
  }

  TimerMode get mode => _mode;
  int get timeLeft => _timeLeft;
  bool get isRunning => _isRunning;
  List<Task> get tasks => _tasks;
  int get totalPomodoros => _totalPomodoros;

  void _loadSettings() async {
    final prefs = await SharedPreferences.getInstance();
    _workDuration = prefs.getInt('workDuration') ?? 25;
    _shortBreakDuration = prefs.getInt('shortBreakDuration') ?? 5;
    _longBreakDuration = prefs.getInt('longBreakDuration') ?? 15;
    _totalPomodoros = prefs.getInt('totalPomodoros') ?? 0;
    resetTimer();
  }

  void saveSettings(int work, int short, int long) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setInt('workDuration', work);
    await prefs.setInt('shortBreakDuration', short);
    await prefs.setInt('longBreakDuration', long);
    _workDuration = work;
    _shortBreakDuration = short;
    _longBreakDuration = long;
    resetTimer();
  }

  void _loadTasks() async {
    _tasks = await DatabaseHelper.instance.readAllTasks();
    notifyListeners();
  }

  void addTask(String title) async {
    final task = Task(title: title);
    await DatabaseHelper.instance.create(task);
    _loadTasks();
  }

  void toggleTask(Task task) async {
    task.isCompleted = !task.isCompleted;
    await DatabaseHelper.instance.update(task);
    _loadTasks();
  }

  void deleteTask(int id) async {
    await DatabaseHelper.instance.delete(id);
    _loadTasks();
  }

  void setMode(TimerMode mode) {
    _mode = mode;
    resetTimer();
  }

  void resetTimer() {
    _timer?.cancel();
    _isRunning = false;
    switch (_mode) {
      case TimerMode.pomodoro:
        _timeLeft = _workDuration * 60;
        break;
      case TimerMode.shortBreak:
        _timeLeft = _shortBreakDuration * 60;
        break;
      case TimerMode.longBreak:
        _timeLeft = _longBreakDuration * 60;
        break;
    }
    notifyListeners();
  }

  void toggleTimer() {
    if (_isRunning) {
      _timer?.cancel();
      _isRunning = false;
    } else {
      _isRunning = true;
      _timer = Timer.periodic(const Duration(seconds: 1), (timer) {
        if (_timeLeft > 0) {
          _timeLeft--;
          notifyListeners();
        } else {
          _handleTimerComplete();
        }
      });
    }
    notifyListeners();
  }

  void _handleTimerComplete() async {
    _timer?.cancel();
    _isRunning = false;

    if (_mode == TimerMode.pomodoro) {
      _totalPomodoros++;
      final prefs = await SharedPreferences.getInstance();
      await prefs.setInt('totalPomodoros', _totalPomodoros);

      // Auto-switch to short break
      _mode = TimerMode.shortBreak;
    } else {
      _mode = TimerMode.pomodoro;
    }
    resetTimer();
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }
}
""")

    # main.dart
    with open(os.path.join(lib_dir, "main.dart"), "w") as f:
        f.write(r"""
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:lottie/lottie.dart';
import 'dart:async';
import 'providers/pomodoro_provider.dart';

void main() {
  runApp(
    ChangeNotifierProvider(
      create: (context) => PomodoroProvider(),
      child: const AtunafsiApp(),
    ),
  );
}

class AtunafsiApp extends StatelessWidget {
  const AtunafsiApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Atunafsi Pomodoro',
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFFE57373)),
        fontFamily: 'Roboto',
      ),
      home: const SplashScreen(),
    );
  }
}

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    super.initState();
    Timer(const Duration(seconds: 3), () {
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(builder: (_) => const HomeScreen()),
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Image.asset('assets/atunafsi.jpg', width: 200, height: 200),
            const SizedBox(height: 20),
            const CircularProgressIndicator(),
          ],
        ),
      ),
    );
  }
}

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Atunafsi'),
        actions: [
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const SettingsScreen()),
              );
            },
          )
        ],
      ),
      body: Column(
        children: [
          const TimerSection(),
          const Expanded(child: TaskListSection()),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          _showAddTaskDialog(context);
        },
        child: const Icon(Icons.add),
      ),
    );
  }

  void _showAddTaskDialog(BuildContext context) {
    final controller = TextEditingController();
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: const Text('Add Task'),
          content: TextField(
            controller: controller,
            decoration: const InputDecoration(hintText: 'Task title'),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Cancel'),
            ),
            TextButton(
              onPressed: () {
                if (controller.text.isNotEmpty) {
                  Provider.of<PomodoroProvider>(context, listen: false)
                      .addTask(controller.text);
                }
                Navigator.pop(context);
              },
              child: const Text('Add'),
            ),
          ],
        );
      },
    );
  }
}

class TimerSection extends StatelessWidget {
  const TimerSection({super.key});

  String _formatTime(int seconds) {
    int minutes = seconds ~/ 60;
    int remainingSeconds = seconds % 60;
    return '${minutes.toString().padLeft(2, '0')}:${remainingSeconds.toString().padLeft(2, '0')}';
  }

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<PomodoroProvider>(context);

    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.primaryContainer,
        borderRadius: const BorderRadius.only(
          bottomLeft: Radius.circular(30),
          bottomRight: Radius.circular(30),
        ),
      ),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              _ModeButton(title: 'Pomodoro', mode: TimerMode.pomodoro, currentMode: provider.mode),
              _ModeButton(title: 'Short Break', mode: TimerMode.shortBreak, currentMode: provider.mode),
              _ModeButton(title: 'Long Break', mode: TimerMode.longBreak, currentMode: provider.mode),
            ],
          ),
          const SizedBox(height: 30),
          Stack(
            alignment: Alignment.center,
            children: [
              if (provider.isRunning)
                SizedBox(
                  width: 250,
                  height: 250,
                  child: Lottie.asset('assets/animation.json', fit: BoxFit.contain),
                ),
              Text(
                _formatTime(provider.timeLeft),
                style: const TextStyle(fontSize: 80, fontWeight: FontWeight.bold),
              ),
            ],
          ),
          const SizedBox(height: 30),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              IconButton(
                iconSize: 64,
                icon: Icon(provider.isRunning ? Icons.pause_circle_filled : Icons.play_circle_filled),
                color: Theme.of(context).colorScheme.primary,
                onPressed: provider.toggleTimer,
              ),
              IconButton(
                iconSize: 48,
                icon: const Icon(Icons.refresh),
                onPressed: provider.resetTimer,
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class _ModeButton extends StatelessWidget {
  final String title;
  final TimerMode mode;
  final TimerMode currentMode;

  const _ModeButton({required this.title, required this.mode, required this.currentMode});

  @override
  Widget build(BuildContext context) {
    final isSelected = mode == currentMode;
    return GestureDetector(
      onTap: () => Provider.of<PomodoroProvider>(context, listen: false).setMode(mode),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
        decoration: BoxDecoration(
          color: isSelected ? Theme.of(context).colorScheme.primary : Colors.transparent,
          borderRadius: BorderRadius.circular(20),
        ),
        child: Text(
          title,
          style: TextStyle(
            color: isSelected ? Theme.of(context).colorScheme.onPrimary : Theme.of(context).colorScheme.onPrimaryContainer,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
    );
  }
}

class TaskListSection extends StatelessWidget {
  const TaskListSection({super.key});

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<PomodoroProvider>(context);

    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Tasks',
            style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 10),
          Expanded(
            child: provider.tasks.isEmpty
                ? const Center(child: Text('No tasks yet. Add one!'))
                : ListView.builder(
                    itemCount: provider.tasks.length,
                    itemBuilder: (context, index) {
                      final task = provider.tasks[index];
                      return Card(
                        child: ListTile(
                          leading: Checkbox(
                            value: task.isCompleted,
                            onChanged: (_) => provider.toggleTask(task),
                          ),
                          title: Text(
                            task.title,
                            style: TextStyle(
                              decoration: task.isCompleted ? TextDecoration.lineThrough : null,
                            ),
                          ),
                          trailing: IconButton(
                            icon: const Icon(Icons.delete),
                            onPressed: () => provider.deleteTask(task.id!),
                          ),
                        ),
                      );
                    },
                  ),
          ),
        ],
      ),
    );
  }
}

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<PomodoroProvider>(context);

    return Scaffold(
      appBar: AppBar(title: const Text('Settings')),
      body: ListView(
        padding: const EdgeInsets.all(16.0),
        children: [
          const Text('Total Pomodoros Completed', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 10),
          Text('${provider.totalPomodoros}', style: const TextStyle(fontSize: 32, color: Colors.red)),
          const Divider(height: 40),
          const Text('Timer Durations (minutes)', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          // Simplified settings for demonstration
          ListTile(
            title: const Text('Reset Settings to Default'),
            trailing: const Icon(Icons.restore),
            onTap: () {
              provider.saveSettings(25, 5, 15);
              ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Settings Reset')));
            },
          ),
        ],
      ),
    );
  }
}
""")

    # 5. Build APK (Skipped in automation due to headless sandbox networking constraints, uncomment to build locally)
    # print("Building APK...")
    # run_cmd(["flutter", "build", "apk", "--debug"], cwd=app_dir)
    # print("Build complete!")

if __name__ == "__main__":
    build_app()
