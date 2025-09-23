#!/usr/bin/env python3
"""
Keyboard Sound Generator
Creates realistic mechanical keyboard sounds programmatically
"""

# Enforce venv: re-exec with local venv Python if not already using it
import os, sys
from pathlib import Path
BASE = Path(__file__).resolve().parent
VENV_PY = BASE / 'venv' / 'bin' / 'python3'
if VENV_PY.exists() and Path(sys.executable) != VENV_PY:
    os.execv(str(VENV_PY), [str(VENV_PY), __file__] + sys.argv[1:])

import numpy as np
import wave
import argparse
from pathlib import Path

class KeyboardSoundGenerator:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate

    def generate_click_sound(self, frequency=800, duration=0.1, click_type="blue"):
        """Generate realistic mechanical keyboard sounds"""
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)

        if click_type == "blue":
            # Cherry MX Blue - realistic click with plastic impact
            # Key press impact (plastic hitting plastic)
            impact_freq = 2000 + np.random.normal(0, 200)
            impact = np.exp(-t * 80) * np.sin(impact_freq * 2 * np.pi * t) * (t < 0.005)

            # Spring click mechanism
            spring_freq = 800 + np.random.normal(0, 50)
            spring_click = np.exp(-t * 40) * np.sin(spring_freq * 2 * np.pi * t) * (t < 0.01)

            # Housing resonance
            housing_freq = 300 + np.random.normal(0, 30)
            housing = np.exp(-t * 12) * np.sin(housing_freq * 2 * np.pi * t)

            # Plastic friction noise
            friction = np.random.normal(0, 0.1, len(t)) * np.exp(-t * 25) * (t < 0.02)

            sound = 0.6 * impact + 0.8 * spring_click + 0.3 * housing + 0.2 * friction

        elif click_type == "brown":
            # Cherry MX Brown - tactile bump without loud click
            # Tactile bump impact (softer)
            bump_freq = 1200 + np.random.normal(0, 100)
            bump = np.exp(-t * 60) * np.sin(bump_freq * 2 * np.pi * t) * (t < 0.008)

            # Stem sliding in housing
            slide_freq = 600 + np.random.normal(0, 40)
            slide = np.exp(-t * 20) * np.sin(slide_freq * 2 * np.pi * t)

            # Bottom out (key hitting bottom)
            bottom_freq = 400 + np.random.normal(0, 50)
            bottom = np.exp(-t * 30) * np.sin(bottom_freq * 2 * np.pi * t) * (t > 0.02) * (t < 0.035)

            # Subtle friction
            friction = np.random.normal(0, 0.05, len(t)) * np.exp(-t * 20)

            sound = 0.7 * bump + 0.4 * slide + 0.5 * bottom + 0.15 * friction

        elif click_type == "red":
            # Cherry MX Red - linear, smooth, quiet
            # Stem movement (no tactile bump)
            stem_freq = 500 + np.random.normal(0, 30)
            stem = np.exp(-t * 15) * np.sin(stem_freq * 2 * np.pi * t)

            # Bottom out impact (muffled)
            bottom_freq = 350 + np.random.normal(0, 40)
            bottom = np.exp(-t * 40) * np.sin(bottom_freq * 2 * np.pi * t) * (t > 0.025) * (t < 0.04)

            # Very subtle friction
            friction = np.random.normal(0, 0.03, len(t)) * np.exp(-t * 18)

            sound = 0.4 * stem + 0.6 * bottom + 0.1 * friction

        elif click_type == "mechanical":
            # Heavy mechanical keyboard (like IBM Model M buckling spring)
            # Spring buckling mechanism
            spring_freq = 1800 + np.random.normal(0, 150)
            spring = np.exp(-t * 50) * np.sin(spring_freq * 2 * np.pi * t) * (t < 0.012)

            # Metal contact impact
            metal_freq = 3000 + np.random.normal(0, 300)
            metal = np.exp(-t * 100) * np.sin(metal_freq * 2 * np.pi * t) * (t < 0.003)

            # Key cap to key cap collision
            keycap_freq = 800 + np.random.normal(0, 80)
            keycap = np.exp(-t * 25) * np.sin(keycap_freq * 2 * np.pi * t)

            # Plate resonance
            plate_freq = 200 + np.random.normal(0, 20)
            plate = np.exp(-t * 8) * np.sin(plate_freq * 2 * np.pi * t)

            # Mechanical noise
            mech_noise = np.random.normal(0, 0.15, len(t)) * np.exp(-t * 30)

            sound = 0.8 * spring + 0.4 * metal + 0.6 * keycap + 0.3 * plate + 0.3 * mech_noise

        elif click_type == "typewriter":
            # Vintage typewriter sound
            envelope = np.exp(-t * 20) * (1 - np.exp(-t * 100))
            sound = np.sin(frequency * 0.5 * 2 * np.pi * t) * envelope
            # Add metallic ping
            ping = 0.3 * np.sin(frequency * 4 * 2 * np.pi * t) * np.exp(-t * 50)
            sound += ping

        elif click_type == "creamy":
            # Creamy smooth click (like lubed switches)
            envelope = np.exp(-t * 8) * (1 - np.exp(-t * 20)) * (1 + 0.1 * np.sin(t * 30))
            sound = np.sin(frequency * 0.9 * 2 * np.pi * t) * envelope
            # Add smooth harmonics
            sound += 0.4 * np.sin(frequency * 1.5 * 2 * np.pi * t) * envelope
            sound += 0.2 * np.sin(frequency * 2.2 * 2 * np.pi * t) * envelope
            # Reduce harsh frequencies for smoothness

        elif click_type == "dry":
            # Dry, unlubricated switches (scratchy)
            # Rough stem movement
            scratch_freq = 1500 + np.random.normal(0, 200)
            scratch = np.exp(-t * 35) * np.sin(scratch_freq * 2 * np.pi * t)

            # Plastic-on-plastic friction
            friction_high = np.random.uniform(-0.2, 0.2, len(t)) * np.exp(-t * 40)
            friction_filter = np.random.uniform(-0.1, 0.1, len(t)) * np.exp(-t * 25)

            # Sharp impact
            impact_freq = 2500 + np.random.normal(0, 300)
            impact = np.exp(-t * 90) * np.sin(impact_freq * 2 * np.pi * t) * (t < 0.004)

            # Housing rattle
            rattle_freq = 700 + np.random.normal(0, 70)
            rattle = np.exp(-t * 20) * np.sin(rattle_freq * 2 * np.pi * t)

            sound = 0.6 * scratch + 0.4 * friction_high + 0.3 * friction_filter + 0.7 * impact + 0.4 * rattle

        elif click_type == "thock":
            # Deep thocky sound (Topre-style or thick keycaps)
            # Deep key impact on thick material
            thock_freq = 250 + np.random.normal(0, 25)
            thock_impact = np.exp(-t * 15) * np.sin(thock_freq * 2 * np.pi * t)

            # Dome compression (Topre-style)
            dome_freq = 400 + np.random.normal(0, 30)
            dome = np.exp(-t * 30) * np.sin(dome_freq * 2 * np.pi * t) * (t < 0.015)

            # Case resonance (deep, wooden)
            case_freq = 120 + np.random.normal(0, 15)
            case_resonance = np.exp(-t * 5) * np.sin(case_freq * 2 * np.pi * t)

            # Muffled high frequencies
            muffled_freq = 1000 + np.random.normal(0, 100)
            muffled = np.exp(-t * 80) * np.sin(muffled_freq * 2 * np.pi * t) * (t < 0.005)

            sound = 0.8 * thock_impact + 0.5 * dome + 0.6 * case_resonance + 0.2 * muffled

        elif click_type == "clicky":
            # Extra clicky sound (like Box Jade/Navy)
            envelope = np.exp(-t * 20) * (1 - np.exp(-t * 80))
            sound = np.sin(frequency * 1.4 * 2 * np.pi * t) * envelope
            # Add multiple click components
            click1 = 0.6 * np.sin(frequency * 4 * 2 * np.pi * t) * np.exp(-t * 100) * (t < 0.02)
            click2 = 0.4 * np.sin(frequency * 6 * 2 * np.pi * t) * np.exp(-t * 120) * (t < 0.015)
            sound += click1 + click2

        elif click_type == "silent":
            # Silent switch sound (dampened)
            envelope = np.exp(-t * 12) * (1 - np.exp(-t * 25))
            sound = np.sin(frequency * 0.7 * 2 * np.pi * t) * envelope
            # Very subtle harmonics
            sound += 0.1 * np.sin(frequency * 1.8 * 2 * np.pi * t) * envelope
            # Reduce overall volume
            sound *= 0.5

        elif click_type == "tactile":
            # Pronounced tactile bump
            envelope = np.exp(-t * 10) * (1 - np.exp(-t * 35))
            # Create tactile bump effect
            bump = (1 + 0.8 * np.exp(-((t - 0.01) / 0.005) ** 2))
            sound = np.sin(frequency * 0.85 * 2 * np.pi * t) * envelope * bump
            sound += 0.3 * np.sin(frequency * 2.3 * 2 * np.pi * t) * envelope

        elif click_type == "lofi":
            # Lofi chill keyboard sound (warm, soft, nostalgic)
            envelope = np.exp(-t * 5) * (1 - np.exp(-t * 12))
            # Warm, muffled base sound
            sound = np.sin(frequency * 0.6 * 2 * np.pi * t) * envelope
            # Add warm harmonics
            sound += 0.3 * np.sin(frequency * 1.2 * 2 * np.pi * t) * envelope
            sound += 0.2 * np.sin(frequency * 0.8 * 2 * np.pi * t) * envelope
            # Add vinyl-like warmth
            warmth = 0.05 * np.sin(frequency * 0.3 * 2 * np.pi * t) * envelope
            sound += warmth
            # Soft tape saturation effect
            sound = np.tanh(sound * 1.5) * 0.7

        elif click_type == "gx_feryn":
            # GX Feryn style (smooth gaming sound)
            envelope = np.exp(-t * 10) * (1 - np.exp(-t * 30))
            sound = np.sin(frequency * 1.0 * 2 * np.pi * t) * envelope
            # Add gaming-optimized harmonics
            sound += 0.4 * np.sin(frequency * 2.1 * 2 * np.pi * t) * envelope
            sound += 0.2 * np.sin(frequency * 3.3 * 2 * np.pi * t) * envelope
            # Add subtle digital processing effect
            digital_effect = 0.1 * np.sin(frequency * 5 * 2 * np.pi * t) * np.exp(-t * 50)
            sound += digital_effect

        elif click_type == "lee_sin":
            # Lee Sin inspired sound (sharp, precise, martial arts-like)
            envelope = np.exp(-t * 25) * (1 - np.exp(-t * 100))
            sound = np.sin(frequency * 1.3 * 2 * np.pi * t) * envelope
            # Add sharp attack like a martial arts strike
            strike = 0.8 * np.sin(frequency * 4 * 2 * np.pi * t) * np.exp(-t * 80) * (t < 0.015)
            sound += strike
            # Add resonant echo
            echo = 0.2 * np.sin(frequency * 1.5 * 2 * np.pi * t) * np.exp(-t * 15) * (t > 0.02)
            sound += echo

        elif click_type == "hacker":
            # Hacker keyboard sound (retro terminal, Matrix-like)
            envelope = np.exp(-t * 15) * (1 - np.exp(-t * 45))
            # Base terminal sound
            sound = np.sin(frequency * 1.1 * 2 * np.pi * t) * envelope
            # Add retro computer harmonics
            sound += 0.4 * np.sin(frequency * 2.7 * 2 * np.pi * t) * envelope
            sound += 0.3 * np.sin(frequency * 4.1 * 2 * np.pi * t) * envelope
            # Add digital glitch effect
            glitch = np.random.choice([-0.1, 0, 0.1], len(sound)) * envelope * 0.3
            sound += glitch
            # Add terminal beep component
            beep = 0.2 * np.sin(frequency * 6 * 2 * np.pi * t) * np.exp(-t * 60) * (t < 0.01)
            sound += beep

        elif click_type == "hard":
            # Extremely hard mechanical keyboard sound (aggressive, loud, sharp)
            # Violent key impact (metal hitting metal)
            impact_freq = 3500 + np.random.normal(0, 400)
            impact = np.exp(-t * 120) * np.sin(impact_freq * 2 * np.pi * t) * (t < 0.003)

            # Aggressive spring compression
            spring_freq = 1200 + np.random.normal(0, 150)
            spring = np.exp(-t * 60) * np.sin(spring_freq * 2 * np.pi * t) * (t < 0.008)

            # Sharp tactile bump (very pronounced)
            bump_freq = 2000 + np.random.normal(0, 200)
            bump = np.exp(-t * 80) * np.sin(bump_freq * 2 * np.pi * t) * (t < 0.006)

            # Hard bottom-out collision
            bottom_freq = 800 + np.random.normal(0, 100)
            bottom = np.exp(-t * 40) * np.sin(bottom_freq * 2 * np.pi * t) * (t > 0.015) * (t < 0.03)

            # Plate vibration/ringing (aggressive)
            plate_freq = 400 + np.random.normal(0, 50)
            plate_ring = np.exp(-t * 20) * np.sin(plate_freq * 2 * np.pi * t)

            # Sharp metallic resonance
            metal_freq = 4000 + np.random.normal(0, 500)
            metal_ring = np.exp(-t * 100) * np.sin(metal_freq * 2 * np.pi * t) * (t < 0.004)

            # Harsh friction and scratching
            scratch = np.random.uniform(-0.3, 0.3, len(t)) * np.exp(-t * 50)

            # Case resonance (deep, aggressive)
            case_freq = 180 + np.random.normal(0, 20)
            case_thump = np.exp(-t * 12) * np.sin(case_freq * 2 * np.pi * t)

            sound = 1.0 * impact + 0.9 * spring + 0.8 * bump + 0.7 * bottom + 0.6 * plate_ring + 0.5 * metal_ring + 0.4 * scratch + 0.5 * case_thump

        # Normalize and apply realistic dynamics
        if np.max(np.abs(sound)) > 0:
            sound = sound / np.max(np.abs(sound)) * 0.7

        # Apply subtle compression for realism
        sound = np.tanh(sound * 1.2) * 0.8

        return sound.astype(np.float32)

    def save_wav(self, sound_data, filename):
        """Save sound data as WAV file"""
        # Convert to 16-bit integers
        sound_int = (sound_data * 32767).astype(np.int16)

        with wave.open(str(filename), 'w') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(sound_int.tobytes())

        print(f"✅ Generated: {filename}")

def main():
    parser = argparse.ArgumentParser(description='Generate keyboard sounds')
    parser.add_argument('--type', choices=['blue', 'brown', 'red', 'mechanical', 'typewriter', 'creamy', 'dry', 'thock', 'clicky', 'silent', 'tactile', 'lofi', 'gx_feryn', 'lee_sin', 'hacker', 'hard', 'all'],
                       default='all', help='Type of keyboard sound to generate')
    parser.add_argument('--duration', type=float, default=0.15, help='Sound duration in seconds')
    parser.add_argument('--frequency', type=int, default=800, help='Base frequency in Hz')
    parser.add_argument('--output', type=str, default='generated_sounds', help='Output directory')

    args = parser.parse_args()

    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)

    generator = KeyboardSoundGenerator()

    if args.type == 'all':
        sound_types = ['blue', 'brown', 'red', 'mechanical', 'typewriter', 'creamy', 'dry', 'thock', 'clicky', 'silent', 'tactile', 'lofi', 'gx_feryn', 'lee_sin', 'hacker', 'hard']
    else:
        sound_types = [args.type]

    print(f"🎵 Generating keyboard sounds...")
    print(f"📁 Output directory: {output_dir}")
    print(f"⏱️  Duration: {args.duration}s")
    print(f"🔊 Base frequency: {args.frequency}Hz")
    print()

    for sound_type in sound_types:
        # Generate sound
        sound = generator.generate_click_sound(
            frequency=args.frequency,
            duration=args.duration,
            click_type=sound_type
        )

        # Save to file
        filename = output_dir / f"keyboard_{sound_type}.wav"
        generator.save_wav(sound, filename)

    print(f"\n🎉 Generated {len(sound_types)} keyboard sounds!")
    print(f"\n💡 Try them with your daemon:")
    print(f"   cp {output_dir}/keyboard_blue.wav key_press.wav")
    print(f"   ./keyboard_sound_control.sh restart")

if __name__ == "__main__":
    main()
