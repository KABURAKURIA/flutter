import os
import subprocess
import sys

# Templates for different app use cases
TEMPLATES = [
    {
        "name": "Simple Hello World",
        "code": """
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
        "code": """
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
        "code": """
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
    }
]

def create_app(app_name, template_index):
    print(f"Creating {app_name}...")

    # Ensure the flutter tool is in path or use the local one
    flutter_bin = os.path.join(os.getcwd(), 'tools', 'flutter', 'bin', 'flutter')
    if not os.path.exists(flutter_bin):
        flutter_bin = 'flutter' # Hope it's in path

    # Run flutter create
    # Using --platforms=web,linux to reduce file count if possible,
    # but 'flutter create' is standard.
    # To save space/time, we can try to minimize, but standard is safest for "real" apps.
    # Added --offline to speed up generation by avoiding network calls for pub get
    cmd = [flutter_bin, 'create', '--offline', app_name]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Error creating app {app_name}: {e.stderr.decode()}")
        return False

    # Inject Template
    template = TEMPLATES[template_index % len(TEMPLATES)]
    main_dart_path = os.path.join(app_name, 'lib', 'main.dart')

    with open(main_dart_path, 'w') as f:
        f.write(template['code'])

    print(f"Successfully created {app_name} with template: {template['name']}")
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_apps.py <number_of_apps> [start_index]")
        sys.exit(1)

    count = int(sys.argv[1])
    start_index = 0
    if len(sys.argv) > 2:
        start_index = int(sys.argv[2])

    for i in range(start_index, start_index + count):
        app_name = f"flutter_app_{i+1:03d}"
        if not create_app(app_name, i):
            print(f"Failed to create {app_name}")

if __name__ == "__main__":
    main()
