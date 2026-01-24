#!/usr/bin/env python3
"""
Demo script to test rate limit handling and show alternative models.

Usage:
    python scripts/test_rate_limit.py
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.utils import get_recommended_model, ALTERNATIVE_MODELS


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def display_current_config():
    """Display current Groq configuration."""
    print_section("📋 Current Configuration")
    
    groq_key = os.getenv("GROQ_API_KEY", "Not set")
    backup_keys = os.getenv("GROQ_API_KEYS_BACKUP", "")
    model = os.getenv("GROQ_MODEL_NAME", "llama-3.3-70b-versatile")
    
    print(f"Primary API Key: {groq_key[:20]}..." if len(groq_key) > 20 else f"Primary API Key: {groq_key}")
    
    if backup_keys:
        backup_list = [k.strip() for k in backup_keys.split(",") if k.strip()]
        print(f"Backup Keys: {len(backup_list)} configured")
        for i, key in enumerate(backup_list, 1):
            masked = f"{key[:10]}...{key[-4:]}" if len(key) > 14 else key
            print(f"  {i}. {masked}")
    else:
        print("Backup Keys: None (⚠️  Consider adding backup keys)")
    
    print(f"\nCurrent Model: {model}")
    
    if model in ALTERNATIVE_MODELS["groq"]:
        limits = ALTERNATIVE_MODELS["groq"][model]
        print(f"  - TPM Limit: {limits['tpm']:,}")
        print(f"  - RPM Limit: {limits['rpm']}")


def display_alternative_models():
    """Display alternative model recommendations."""
    print_section("🚀 Alternative Free Models")
    
    recommendations = get_recommended_model()
    
    print("1️⃣  SAME PROVIDER (Groq - Easy Switch)")
    rec = recommendations["same_provider"]
    print(f"   Model: {rec['model']}")
    print(f"   Reason: {rec['reason']}")
    print(f"   TPM: {rec['limits']['tpm']:,} | RPM: {rec['limits']['rpm']}")
    print(f"\n   How to use:")
    print(f"   Add to .env: GROQ_MODEL_NAME={rec['model']}\n")
    
    print("2️⃣  BEST FREE OPTION (Recommended!)")
    rec = recommendations["best_free"]
    print(f"   Model: {rec['model']}")
    print(f"   Provider: {rec['provider']}")
    print(f"   Reason: {rec['reason']}")
    print(f"   TPM: {rec['limits']['tpm']:,} | RPM: {rec['limits']['rpm']}")
    print(f"\n   How to use:")
    print(f"   1. Get API key: https://aistudio.google.com/apikey")
    print(f"   2. Add to .env:")
    print(f"      GOOGLE_API_KEY=your_key_here")
    print(f"      GROQ_MODEL_NAME={rec['model']}\n")
    
    print("3️⃣  BALANCED OPTION")
    rec = recommendations["balanced"]
    print(f"   Model: {rec['model']}")
    print(f"   Provider: {rec['provider']}")
    print(f"   Reason: {rec['reason']}")
    print(f"   TPM: {rec['limits']['tpm']:,} | RPM: {rec['limits']['rpm']}")
    print(f"\n   How to use:")
    print(f"   1. Get API key: https://openrouter.ai/keys")
    print(f"   2. Add to .env:")
    print(f"      OPENROUTER_API_KEY=your_key_here")
    print(f"      GROQ_MODEL_NAME={rec['model']}\n")


def display_all_models():
    """Display all available models."""
    print_section("📊 All Available Free Models")
    
    for provider, models in ALTERNATIVE_MODELS.items():
        print(f"\n{provider.upper()}:")
        for model_name, limits in models.items():
            tpm = f"{limits['tpm']:,}".rjust(10)
            rpm = str(limits['rpm']).rjust(3)
            print(f"  • {model_name:30} | TPM: {tpm} | RPM: {rpm}")


def display_quick_fixes():
    """Display quick fix recommendations."""
    print_section("⚡ Quick Fixes for Rate Limit")
    
    print("OPTION 1: Add Backup API Keys (Easiest)")
    print("-" * 70)
    print("1. Create 2-3 more API keys at: https://console.groq.com/keys")
    print("2. Add to .env:")
    print("   GROQ_API_KEYS_BACKUP=key2,key3,key4")
    print("3. System will auto-rotate when hitting rate limit\n")
    
    print("OPTION 2: Switch to Faster Model (Same Provider)")
    print("-" * 70)
    print("1. Update .env:")
    print("   GROQ_MODEL_NAME=llama-3.1-8b-instant")
    print("2. Restart backend")
    print("3. Enjoy 67% higher TPM limit (20k vs 12k)\n")
    
    print("OPTION 3: Use Google Gemini (Highest Limit)")
    print("-" * 70)
    print("1. Get free API key: https://aistudio.google.com/apikey")
    print("2. Update .env:")
    print("   GOOGLE_API_KEY=your_key_here")
    print("   GROQ_MODEL_NAME=gemini-1.5-flash")
    print("3. Restart backend")
    print("4. Enjoy 250k TPM (20x higher!)\n")
    
    print("OPTION 4: Use Rate Limit Handler (Already Implemented)")
    print("-" * 70)
    print("1. Update service/src/api.py:")
    print("   from src.utils import prepare_interview_with_retry")
    print("2. Replace prepare_for_interview with prepare_interview_with_retry")
    print("3. System will auto-retry with exponential backoff\n")


def main():
    """Main function."""
    print("\n" + "="*70)
    print("  🔍 AI Mock Interview Agent - Rate Limit Analysis")
    print("="*70)
    
    display_current_config()
    display_alternative_models()
    display_all_models()
    display_quick_fixes()
    
    print("\n" + "="*70)
    print("  📚 For detailed guide, see: RATE_LIMIT_GUIDE.md")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
