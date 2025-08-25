import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(const ForgivenessApp());
}

class ForgivenessApp extends StatelessWidget {
  const ForgivenessApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: "AI Forgiveness Recommender",
      theme: ThemeData(primarySwatch: Colors.teal, fontFamily: "Arial"),
      home: const SplashScreen(),
    );
  }
}

class SplashScreen extends StatelessWidget {
  const SplashScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.lightBlue[100],
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Image.asset("assets/images/bird.png", height: 150),
            const SizedBox(height: 20),
            const Text(
              "AI Forgiveness Recommender",
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const Spacer(),
            Padding(
              padding: const EdgeInsets.all(20.0),
              child: ElevatedButton(
                onPressed: () {
                  Navigator.pushReplacement(
                    context,
                    MaterialPageRoute(builder: (_) => const InputScreen()),
                  );
                },
                style: ElevatedButton.styleFrom(
                  minimumSize: const Size(double.infinity, 50),
                  backgroundColor: Colors.teal,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
                child: const Text("Enter"),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class InputScreen extends StatefulWidget {
  const InputScreen({super.key});

  @override
  State<InputScreen> createState() => _InputScreenState();
}

class _InputScreenState extends State<InputScreen> {
  final TextEditingController conflictController = TextEditingController();
  String? selectedReligion;

  // Function to get forgiveness advice from Flask API
  Future<String> getForgivenessAdvice(
    String conflictDescription,
    String religion,
  ) async {
    final url = Uri.parse('http://192.168.0.102:5000/get_advice');

    try {
      final response = await http.post(
        url,
        headers: {"Content-Type": "application/json"},
        body: json.encode({
          'conflict_description': conflictDescription,
          'religion': religion,
        }),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return data['advice'] ?? 'No advice found.';
      } else {
        return 'Error: Unable to get advice from the server.';
      }
    } catch (e) {
      return 'Error: Unable to reach the server.';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("AI Forgiveness Recommender")),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            TextField(
              controller: conflictController,
              decoration: InputDecoration(
                hintText: "Describe your conflict...",
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
              maxLines: 3,
            ),
            const SizedBox(height: 20),
            DropdownButtonFormField<String>(
              decoration: InputDecoration(
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
              value: selectedReligion,
              hint: const Text("Choose Religion"),
              onChanged: (value) {
                setState(() {
                  selectedReligion = value;
                });
              },
              items:
                  ["General", "Christianity", "Islam", "Hinduism", "Buddhism"]
                      .map(
                        (religion) => DropdownMenuItem(
                          value: religion,
                          child: Text(religion),
                        ),
                      )
                      .toList(),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () async {
                final conflictDescription = conflictController.text;
                if (conflictDescription.isNotEmpty &&
                    selectedReligion != null) {
                  final advice = await getForgivenessAdvice(
                    conflictDescription,
                    selectedReligion!,
                  );
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => AdviceScreen(advice: advice),
                    ),
                  );
                } else {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(
                      content: Text(
                        "Please provide both conflict and religion.",
                      ),
                    ),
                  );
                }
              },
              style: ElevatedButton.styleFrom(
                minimumSize: const Size(double.infinity, 50),
                backgroundColor: Colors.teal,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
              child: const Text("Get Forgiveness Advice"),
            ),
          ],
        ),
      ),
    );
  }
}

class AdviceScreen extends StatelessWidget {
  final String advice;
  const AdviceScreen({super.key, required this.advice});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Forgiveness Advice")),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [Text(advice, style: const TextStyle(fontSize: 18))],
        ),
      ),
    );
  }
}
