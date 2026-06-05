# Poradnik: Instalacja ROS 2 ze źródeł na Linux Mint & Ubuntu

Oficjalny poradnik instalacji ROS 2 (wersja Jazzy Jalisco) skompilowany ze źródeł, dostosowany specjalnie dla systemów Linux Mint oraz Ubuntu.

> [!NOTE]
> Czytasz dokumentację starszej, ale wciąż wspieranej wersji ROS 2. Aby uzyskać informacje o najnowszej wersji, zapoznaj się z wersją **Lyrical**.

---

## Spis treści
1. [Wymagania systemowe](#1-wymagania-systemowe)
2. [Konfiguracja systemu](#2-konfiguracja-systemu)
   - [Ustawienia regionalne (Locale)](#ustawienia-regionalne-locale)
   - [Włączenie wymaganych repozytoriów](#włączenie-wymaganych-repozytoriów)
   - [Instalacja narzędzi programistycznych](#instalacja-narzędzi-programistycznych)
3. [Budowanie ROS 2](#3-budowanie-ros-2)
   - [Pobieranie kodu źródłowego](#pobieranie-kodu-źródłowego)
   - [Instalacja zależności przy użyciu rosdep](#instalacja-zależności-przy-użyciu-rosdep)
   - [Kompilacja kodu](#kompilacja-kodu-w-przestrzeni-roboczej)
4. [Konfiguracja środowiska](#4-konfiguracja-środowiska)
5. [Uruchomienie przykładowych aplikacji](#5-uruchomienie-przykładowych-aplikacji)
6. [Alternatywne kompilatory (Clang)](#6-alternatywne-kompilatory-clang)
7. [Odinstalowanie środowiska](#7-odinstalowanie-środowiska)

---

## 1. Wymagania systemowe

Obecne platformy docelowe oparte na Debianie dla **Jazzy Jalisco** to:
- **Poziom 1:** Ubuntu Linux - Noble (24.04) 64-bit
- **Poziom 3:** Ubuntu Linux - Jammy (22.04) 64-bit
- **Poziom 3:** Debian Linux - Bookworm (12) 64-bit

Zgodnie ze specyfikacją zdefiniowaną w **REP 2000**.

---

## 2. Konfiguracja systemu

### Ustawienia regionalne (Locale)
Upewnij się, że Twój system obsługuje kodowanie UTF-8. W minimalnych środowiskach (np. Docker) kodowanie może być ustawione domyślnie na POSIX.

```bash
locale

sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

locale
```

### Włączenie wymaganych repozytoriów
Dodaj oficjalne repozytorium apt ROS 2 do swojego systemu. Najpierw aktywuj repozytorium **Ubuntu Universe**:

```bash
sudo apt install software-properties-common
sudo add-apt-repository universe
```

Następnie pobierz i zainstaluj klucze oraz konfigurację źródeł poprzez pakiet ros2-apt-source:

```bash
sudo apt update && sudo apt install curl -y
export ROS_APT_SOURCE_VERSION=$(curl -s [https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest](https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest) | grep -F "tag_name" | awk -F'"' '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb "[https://github.com/ros-infrastructure/ros-apt-source/releases/download/$](https://github.com/ros-infrastructure/ros-apt-source/releases/download/$){ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb
```

### Instalacja narzędzi programistycznych
Zainstaluj pakiety deweloperskie niezbędne do pobrania i skompilowania ROS 2:

```bash
sudo apt update && sudo apt install -y \
  python3-flake8-blind-except \
  python3-flake8-class-newline \
  python3-flake8-deprecated \
  python3-mypy \
  python3-pip \
  python3-pytest \
  python3-pytest-cov \
  python3-pytest-mock \
  python3-pytest-repeat \
  python3-pytest-rerunfailures \
  python3-pytest-runner \
  python3-pytest-timeout \
  ros-dev-tools
```

---

## 3. Budowanie ROS 2

### Pobieranie kodu źródłowego
Utwórz dedykowany katalog przestrzeni roboczej (workspace) i pobierz repozytoria:

```bash
mkdir -p ~/ros2_jazzy/src
cd ~/ros2_jazzy
vcs import --input [https://raw.githubusercontent.com/ros2/ros2/jazzy/ros2.repos](https://raw.githubusercontent.com/ros2/ros2/jazzy/ros2.repos) src
```

### Instalacja zależności przy użyciu rosdep
Przed zainstalowaniem zależności upewnij się, że Twój system operacyjny posiada zaktualizowane pakiety.

```bash
sudo apt upgrade
sudo rosdep init
rosdep update
rosdep install --from-paths src --ignore-src -y --skip-keys "fastcdr rti-connext-dds-6.0.1 urdfdom_headers"
```

> [!WARNING]
> Jeśli używasz dystrybucji opierającej się na Ubuntu, która nie identyfikuje się bezpośrednio jako Ubuntu (**takiej jak Linux Mint**), menedżer rosdep zwróci błąd `Unsupported OS [mint]`. W takim przypadku musisz wymusić system docelowy poprzez dodanie flagi `--os=ubuntu:noble` do powyższego polecenia instalacji zależności:

```bash
rosdep install --from-paths src --ignore-src -y --skip-keys "fastcdr rti-connext-dds-6.0.1 urdfdom_headers" --os=ubuntu:noble
```

### Dodatkowe implementacje RMW (Opcjonalnie)
Domyślnym oprogramowaniem pośredniczącym (middleware) używanym przez ROS 2 jest **Fast DDS**. Istnieje możliwość zmiany implementacji RMW podczas kompilacji lub w czasie uruchamiania aplikacji.

### Instalacja colcon mixins

```bash
colcon mixin add default [https://github.com/colcon/colcon-mixin-repository/raw/master/index.yaml](https://github.com/colcon/colcon-mixin-repository/raw/master/index.yaml)
colcon mixin update default
```

### Kompilacja kodu w przestrzeni roboczej
Przed budowaniem upewnij się, że środowisko terminala jest "czyste" i nie posiada załadowanych innych wersji ROS 2 (np. wersji binarnych). Polecenie `printenv | grep -i ROS` powinno zwracać pusty wynik.

```bash
cd ~/ros2_jazzy/
colcon build --symlink-install --mixin release
```

> [!NOTE]
> W przypadku problemów z kompilacją niektórych przykładów, możesz wykluczyć kłopotliwe pakiety za pomocą flagi `--packages-skip`. Przykładowo, aby pominąć pakiety zależne od dużej biblioteki OpenCV:

```bash
colcon build --symlink-install --packages-skip image_tools intra_process_demo
```

---

## 4. Konfiguracja środowiska

Aby aktywować nowo zbudowane środowisko ROS 2 w danym oknie terminala, wykonaj:

```bash
. ~/ros2_jazzy/install/local_setup.bash
```

> [!NOTE]
> Jeśli korzystasz z innej powłoki systemowej niż Bash, podmień rozszerzenie `.bash` na właściwy plik konfiguracyjny (np. `setup.sh`, `setup.zsh`).

---

## 5. Uruchomienie przykładowych aplikacji

Przetestuj poprawność działania komunikacji.

W **pierwszym oknie terminala** załaduj konfigurację i uruchom węzeł nadawcy (C++):

```bash
. ~/ros2_jazzy/install/local_setup.bash
ros2 run demo_nodes_cpp talker
```

W **drugim oknie terminala** załaduj konfigurację i uruchom węzeł odbiorcy (Python):

```bash
. ~/ros2_jazzy/install/local_setup.bash
ros2 run demo_nodes_py listener
```

Prawidłowo działające środowisko wyświetli komunikat `Publishing messages` w oknie nadawcy oraz `I heard those messages` w oknie odbiorcy.

---

## 6. Alternatywne kompilatory (Clang)

W celu zmiany domyślnego kompilatora `gcc` na `Clang`, ustaw zmienne środowiskowe i wymuś pełną rekonfigurację narzędzia CMake:

```bash
sudo apt install clang
export CC=clang
export CXX=clang++
colcon build --cmake-force-configure
```

---

## 7. Odinstalowanie środowiska

Aby "odinstalować" środowisko, wystarczy uruchomić nowy terminal bez wczytywania pliku `local_setup.bash`. Jeśli chcesz dodatkowo usunąć pliki z dysku i zwolnić miejsce, usuń cały katalog przestrzeni roboczej:

```bash
rm -rf ~/ros2_jazzy
```
