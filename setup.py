#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup-skript för Longevity Receptgenerator.
Detta skript hjälper dig att konfigurera och testa projektet.
"""

import os
import sys
import shutil
import webbrowser
import subprocess
import time
from pathlib import Path

def create_env_file():
    """Skapar en .env-fil om den inte redan finns"""
    env_path = Path('.env')
    env_example_path = Path('env.example')
    
    if env_path.exists():
        print("✅ .env-fil finns redan")
    else:
        if env_example_path.exists():
            shutil.copy(env_example_path, env_path)
            print("✅ .env-fil skapad från env.example")
            print("⚠️  Glöm inte att uppdatera .env-filen med din OpenAI API-nyckel!")
        else:
            # Skapa en ny .env-fil från grunden
            with open(env_path, 'w', encoding='utf-8') as f:
                f.write("# API-nycklar\n")
                f.write("OPENAI_API_KEY=din_openai_api_nyckel_här\n\n")
                f.write("# Server-konfiguration\n")
                f.write("PORT=8000\n")
            print("✅ .env-fil skapad")
            print("⚠️  Glöm inte att uppdatera .env-filen med din OpenAI API-nyckel!")

def check_api_key():
    """Kontrollerar om OpenAI API-nyckeln är satt"""
    env_path = Path('.env')
    if not env_path.exists():
        return False
    
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('OPENAI_API_KEY='):
                key = line.strip().split('=', 1)[1]
                if key and key != 'din_openai_api_nyckel_här':
                    return True
    return False

def create_test_files():
    """Skapar testfiler för att testa API:et"""
    # Skapa en mapp för testfiler om den inte finns
    test_dir = Path('testdata')
    test_dir.mkdir(exist_ok=True)
    
    # Skapa en exempelfil med ingredienser
    ingredients_path = test_dir / 'ingredienser.txt'
    if not ingredients_path.exists():
        with open(ingredients_path, 'w', encoding='utf-8') as f:
            f.write("""Lax
Quinoa
Grönkål
Rucola
Körsbärstomater
Gurka
Rödlök
Fetaost
Kalamataoliver
Valnötter
Citron
Vitlök
Honungsmelon
Blåbär
Havregryn
Mandelmjölk
Mandlar
Chiafrön
Linfröolja
Ägg
Morötter
Broccoli
Spenat
Svarta bönor
Kikärtor
Fullkornsris
Röda linser
Tofu
Avokado
Zucchini
""")
        print(f"✅ Testfil skapad: {ingredients_path}")
    else:
        print(f"✅ Testfil finns redan: {ingredients_path}")

def install_dependencies():
    """Installerar projektets beroenden"""
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        print("✅ Beroenden installerade")
    except subprocess.CalledProcessError:
        print("❌ Fel vid installation av beroenden")
        return False
    return True

def check_environment():
    """Kontrollerar om miljön är korrekt konfigurerad"""
    # Kontrollera att Python är installerat
    print(f"Python-version: {sys.version}")
    
    # Kontrollera att pip är installerat
    try:
        subprocess.run([sys.executable, '-m', 'pip', '--version'], check=True, capture_output=True)
        print("✅ pip är installerat")
    except subprocess.CalledProcessError:
        print("❌ pip är inte installerat")
        return False
    
    return True

def start_services():
    """Startar API-servern och webbservern"""
    print("\n🚀 Startar tjänsterna...")
    
    # Starta API-servern i en separat process
    api_process = subprocess.Popen([sys.executable, 'api.py'], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE,
                                  text=True)
    
    # Vänta lite för att API-servern ska starta
    print("⏳ Väntar på att API-servern ska starta...")
    time.sleep(3)
    
    # Kontrollera om API-servern startade korrekt
    if api_process.poll() is not None:
        print("❌ API-servern kunde inte startas")
        stdout, stderr = api_process.communicate()
        print(f"Fel: {stderr}")
        return
    
    print("✅ API-server startad på http://localhost:8000")
    
    # Starta webbservern
    print("🌐 Öppnar webbläsaren...")
    webbrowser.open('http://localhost:8000/docs')  # Öppna API-dokumentationen
    
    # Vänta lite till innan vi öppnar frontend
    time.sleep(2)
    
    # Starta frontend-servern och öppna webbläsaren
    subprocess.Popen([sys.executable, 'serve.py'])
    
    print("\n✨ Alla tjänster startade! Du kan nu använda Longevity Receptgenerator.")
    print("📊 API-dokumentation: http://localhost:8000/docs")
    print("🖥️  Frontend: http://localhost:8080")
    print("\nTryck Ctrl+C för att avsluta")
    
    try:
        # Håll processen vid liv tills användaren trycker Ctrl+C
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Avslutar tjänsterna...")
        api_process.terminate()
        print("✅ Tjänsterna avslutade")

def main():
    """Huvudfunktion"""
    print("\n🍽️  Longevity Receptgenerator - Setup 🍽️\n")
    
    # Kontrollera miljön
    if not check_environment():
        print("❌ Miljön är inte korrekt konfigurerad")
        return
    
    # Skapa .env-fil
    create_env_file()
    
    # Installera beroenden
    if not install_dependencies():
        return
    
    # Skapa testfiler
    create_test_files()
    
    # Kontrollera API-nyckel
    if not check_api_key():
        print("\n⚠️  OpenAI API-nyckeln är inte konfigurerad.")
        print("Öppna .env-filen och lägg till din API-nyckel:")
        print("OPENAI_API_KEY=sk-din-api-nyckel-här")
        
        choice = input("\nVill du konfigurera API-nyckeln nu? (j/n): ")
        if choice.lower() in ('j', 'ja', 'y', 'yes'):
            api_key = input("Ange din OpenAI API-nyckel: ")
            with open('.env', 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            with open('.env', 'w', encoding='utf-8') as f:
                for line in lines:
                    if line.startswith('OPENAI_API_KEY='):
                        f.write(f'OPENAI_API_KEY={api_key}\n')
                    else:
                        f.write(line)
            print("✅ API-nyckel konfigurerad")
        else:
            print("\n⚠️  Du måste konfigurera API-nyckeln innan du kan använda API:et")
            return
    
    print("\n✅ Konfiguration slutförd")
    
    # Fråga om användaren vill starta tjänsterna
    choice = input("\nVill du starta API-servern och webbservern nu? (j/n): ")
    if choice.lower() in ('j', 'ja', 'y', 'yes'):
        start_services()

if __name__ == "__main__":
    main() 