# Projekt Testowy - Intel RealSense SR300: Detekcja i Wymiarowanie Skał

*English description below*

## Opis projektu
Niniejszy projekt jest projektem testowym realizowanym przy użyciu kamery głębi Intel RealSense SR300. Głównym celem systemu jest integracja strumienia wizyjnego oraz danych o głębi z modelem sztucznej inteligencji (AI) w celu automatycznego wykrywania skał oraz precyzyjnego określania ich wymiarów w przestrzeni trójwymiarowej.

### Główne funkcjonalności
- **Obsługa kamery RealSense SR300:** Uruchomienie urządzenia, konfiguracja oraz jednoczesne przechwytywanie strumienia RGB i mapy głębi.
- **Model AI do detekcji skał:** Wykorzystanie sieci neuronowej dedykowanej do rozpoznawania i lokalizowania obiektów (skał) na obrazie w czasie rzeczywistym.
- **Wymiarowanie obiektów:** Algorytm obliczający rzeczywiste wymiary (szerokość, wysokość, głębokość) wykrytych skał na podstawie powiązanych danych z sensora głębi.

### Instrukcja instalacji ROS
W repozytorium znajduje się dedykowany katalog zawierający kompletną, spolszczoną dokumentację dotyczącą konfiguracji środowiska:
- **Katalog:** `Poradnik-PL-Instalacja`
- **Zawartość:** Szczegółowa instrukcja instalacji i konfiguracji systemu ROS (Robot Operating System) krok po kroku.

---

# Test Project - Intel RealSense SR300: Rock Detection and Dimensioning

## Project Overview
This is a test project developed using the Intel RealSense SR300 depth camera. The primary objective of the system is to integrate the video stream and depth data with an artificial intelligence (AI) model to automatically detect rocks and precisely determine their dimensions in 3D space.

### Key Features
- **RealSense SR300 Support:** Launching the device, configuring settings, and simultaneously capturing the RGB stream and depth map.
- **AI Model for Rock Detection:** Utilizing a neural network tailored for real-time recognition and localization of objects (rocks) in the frame.
- **Object Dimensioning:** An algorithm that calculates the actual physical dimensions (width, height, depth) of the detected rocks using the corresponding depth sensor data.

### ROS Installation Guide
The repository includes a dedicated directory containing complete documentation for the environment setup:
- **Directory:** `Poradnik-PL-Instalacja`
- **Content:** A comprehensive, step-by-step ROS (Robot Operating System) installation and configuration guide written in Polish.
