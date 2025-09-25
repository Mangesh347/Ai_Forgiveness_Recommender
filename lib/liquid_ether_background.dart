import 'package:flutter/material.dart';
import 'package:animated_background/animated_background.dart';
import 'package:simple_animations/simple_animations.dart';

class LiquidEtherBackground extends StatelessWidget {
  final Widget child;
  final TickerProvider vsync;

  const LiquidEtherBackground({
    Key? key,
    required this.child,
    required this.vsync,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        // 🌈 Layer 1: Animated Gradient Waves
        Positioned.fill(child: _AnimatedGradient()),

        // ✨ Layer 2: Floating Particles
        Positioned.fill(
          child: AnimatedBackground(
            behaviour: RandomParticleBehaviour(
              options: ParticleOptions(
                baseColor: Colors.blueAccent.shade200,
                spawnOpacity: 0.4,
                opacityChangeRate: 0.25,
                minOpacity: 0.1,
                maxOpacity: 0.6,
                particleCount: 60,
                spawnMinSpeed: 15.0,
                spawnMaxSpeed: 30.0,
                spawnMinRadius: 30.0,
                spawnMaxRadius: 70.0,
              ),
            ),
            vsync: vsync,
            child: Container(),
          ),
        ),

        // 🎯 Layer 3: Foreground Content (Login/Signup card)
        child,
      ],
    );
  }
}

/// Internal widget for gradient animation
class _AnimatedGradient extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MirrorAnimationBuilder<Color?>(
      tween: ColorTween(begin: Colors.deepPurple, end: Colors.blueAccent),
      duration: Duration(seconds: 5),
      builder: (context, value, child) {
        return Container(
          decoration: BoxDecoration(
            gradient: RadialGradient(
              colors: [value!, Colors.black],
              center: Alignment(0.3, -0.3),
              radius: 1.2,
            ),
          ),
        );
      },
    );
  }
}
