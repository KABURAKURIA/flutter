import os
import subprocess
import sys
import shutil

# Templates for different app use cases
TEMPLATES = [
    {
        "name": "Simple Hello World",
        "code": r"""
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Hello World',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: Scaffold(
        appBar: AppBar(title: const Text('Hello World App')),
        body: const Center(
          child: Text(
            'Hello, Flutter!',
            style: TextStyle(fontSize: 24),
          ),
        ),
      ),
    );
  }
}
"""
    },
    {
        "name": "Counter App",
        "code": r"""
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Counter App',
      theme: ThemeData(primarySwatch: Colors.green),
      home: const MyHomePage(title: 'Flutter Counter Home Page'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});
  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _counter = 0;

  void _incrementCounter() {
    setState(() {
      _counter++;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(widget.title)),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            const Text('You have pushed the button this many times:'),
            Text(
              '$_counter',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _incrementCounter,
        tooltip: 'Increment',
        child: const Icon(Icons.add),
      ),
    );
  }
}
"""
    },
    {
        "name": "Color Changer",
        "code": r"""
import 'package:flutter/material.dart';
import 'dart:math';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Color Changer',
      home: const ColorChangerPage(),
    );
  }
}

class ColorChangerPage extends StatefulWidget {
  const ColorChangerPage({super.key});

  @override
  State<ColorChangerPage> createState() => _ColorChangerPageState();
}

class _ColorChangerPageState extends State<ColorChangerPage> {
  Color _color = Colors.white;
  final Random _random = Random();

  void _changeColor() {
    setState(() {
      _color = Color.fromRGBO(
        _random.nextInt(256),
        _random.nextInt(256),
        _random.nextInt(256),
        1,
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: _color,
      appBar: AppBar(title: const Text('Tap to Change Color')),
      body: InkWell(
        onTap: _changeColor,
        child: Center(
          child: Container(
            padding: const EdgeInsets.all(20),
            color: Colors.white.withOpacity(0.8),
            child: const Text(
              'Tap anywhere!',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
          ),
        ),
      ),
    );
  }
}
"""
    },
    {
        "name": "Todo List",
        "code": r"""
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Todo List',
      home: const TodoListPage(),
    );
  }
}

class TodoListPage extends StatefulWidget {
  const TodoListPage({super.key});

  @override
  State<TodoListPage> createState() => _TodoListPageState();
}

class _TodoListPageState extends State<TodoListPage> {
  final List<String> _todos = [];
  final TextEditingController _controller = TextEditingController();

  void _addTodo() {
    if (_controller.text.isNotEmpty) {
      setState(() {
        _todos.add(_controller.text);
        _controller.clear();
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Todo List')),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    decoration: const InputDecoration(hintText: 'Enter a task'),
                  ),
                ),
                IconButton(icon: const Icon(Icons.add), onPressed: _addTodo),
              ],
            ),
          ),
          Expanded(
            child: ListView.builder(
              itemCount: _todos.length,
              itemBuilder: (context, index) {
                return ListTile(title: Text(_todos[index]));
              },
            ),
          ),
        ],
      ),
    );
  }
}
"""
    },
    {
        "name": "Login Screen",
        "code": r"""
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Login Screen',
      home: const LoginPage(),
    );
  }
}

class LoginPage extends StatelessWidget {
  const LoginPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Login')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const TextField(decoration: InputDecoration(labelText: 'Username')),
            const TextField(
              decoration: InputDecoration(labelText: 'Password'),
              obscureText: true,
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {},
              child: const Text('Login'),
            ),
          ],
        ),
      ),
    );
  }
}
"""
    },
    {
        "name": "Profile Page",
        "code": r"""
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Profile Page',
      home: const ProfilePage(),
    );
  }
}

class ProfilePage extends StatelessWidget {
  const ProfilePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Profile')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: const [
            CircleAvatar(radius: 50, child: Icon(Icons.person, size: 50)),
            SizedBox(height: 20),
            Text('John Doe', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
            Text('Software Engineer', style: TextStyle(fontSize: 16, color: Colors.grey)),
          ],
        ),
      ),
    );
  }
}
"""
    },
    {
        "name": "Settings Page",
        "code": r"""
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Settings Page',
      home: const SettingsPage(),
    );
  }
}

class SettingsPage extends StatefulWidget {
  const SettingsPage({super.key});

  @override
  State<SettingsPage> createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  bool _notifications = true;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Settings')),
      body: ListView(
        children: [
          SwitchListTile(
            title: const Text('Enable Notifications'),
            value: _notifications,
            onChanged: (bool value) {
              setState(() {
                _notifications = value;
              });
            },
          ),
          ListTile(
            title: const Text('Privacy Policy'),
            onTap: () {},
          ),
        ],
      ),
    );
  }
}
"""
    },
    {
        "name": "Product List",
        "code": r"""
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Product List',
      home: const ProductListPage(),
    );
  }
}

class ProductListPage extends StatelessWidget {
  const ProductListPage({super.key});

  @override
  Widget build(BuildContext context) {
    final List<String> products = List.generate(20, (index) => 'Product ${index + 1}');

    return Scaffold(
      appBar: AppBar(title: const Text('Products')),
      body: ListView.builder(
        itemCount: products.length,
        itemBuilder: (context, index) {
          return Card(
            child: ListTile(
              leading: const Icon(Icons.shopping_cart),
              title: Text(products[index]),
              subtitle: Text('\$${(index + 1) * 10}'),
            ),
          );
        },
      ),
    );
  }
}
"""
    }
]

def get_next_index(out_dir):
    max_index = 0
    # Prioritize the global index file to ensure uniqueness across folders
    global_index_file = '.global_app_index'
    if os.path.exists(global_index_file):
        try:
            with open(global_index_file, 'r') as f:
                max_index = int(f.read().strip())
                return max_index
        except ValueError:
            pass

    # Fallback to local directory check
    if os.path.exists(out_dir):
        for entry in os.listdir(out_dir):
            if entry.startswith('flutter_app_') and os.path.isdir(os.path.join(out_dir, entry)):
                try:
                    idx = int(entry.replace('flutter_app_', ''))
                    if idx > max_index:
                        max_index = idx
                except ValueError:
                    pass
    return max_index

def create_app(out_dir, app_name, template_index, is_first, app_index):
    print(f"Creating {app_name}...")

    flutter_bin = os.path.join(os.getcwd(), 'tools', 'flutter', 'bin', 'flutter')
    if not os.path.exists(flutter_bin):
        flutter_bin = 'flutter'

    app_path = os.path.join(out_dir, app_name)

    cmd = [flutter_bin, 'create', '--platforms=web,linux']
    if not is_first:
        cmd.append('--offline')
    cmd.append(app_name)

    try:
        # Run flutter create in out_dir
        subprocess.run(cmd, cwd=out_dir, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Error creating app {app_name}: {e.stderr.decode()}")
        return False

    # Remove test directory
    test_dir = os.path.join(app_path, 'test')
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

    template = TEMPLATES[template_index % len(TEMPLATES)]
    main_dart_path = os.path.join(app_path, 'lib', 'main.dart')

    import re
    # Robustly replace the title string, handling single/double quotes and capturing the original title
    code_str = re.sub(r"title:\s*['\"](.*?)['\"]", f"title: 'App {app_index} - \\1'", template['code'])

    with open(main_dart_path, 'w') as f:
        f.write(code_str)

    print(f"Successfully created {app_name} with template: {template['name']}")
    return True

def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_apps.py <number_of_apps> <output_directory> [start_index]")
        sys.exit(1)

    count = int(sys.argv[1])
    out_dir = sys.argv[2]

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    if len(sys.argv) > 3:
        start_index = int(sys.argv[3])
    else:
        start_index = get_next_index(out_dir)

    max_idx = start_index
    for i in range(count):
        idx = start_index + i + 1
        max_idx = idx
        app_name = f"flutter_app_{idx:03d}"
        is_first = (i == 0)

        # Determine the correct template index to avoid repeat when restarting
        template_index = (idx - 1) % len(TEMPLATES)

        if not create_app(out_dir, app_name, template_index, is_first, idx):
            print(f"Failed to create {app_name}")

    # Save the global max index
    with open('.global_app_index', 'w') as f:
        f.write(str(max_idx))

if __name__ == "__main__":
    main()
