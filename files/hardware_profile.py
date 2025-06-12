import json
import platform
import os
import subprocess

def get_cpu_info():
    cpu = {
        "cpu_processor": str(platform.processor() or "unknown"),
        "cpu_cores": str(os.cpu_count() or "unknown"),
        "cpu_max_frequency_ghz": "unknown"
    }
    try:
        if os.path.exists("/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq"):
            with open("/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq", "r") as f:
                cpu["cpu_max_frequency_ghz"] = str(round(int(f.read().strip()) / 1000000, 2))
        elif os.path.exists("/proc/cpuinfo"):
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if line.startswith("model name"):
                        parts = line.split("@")
                        if len(parts) > 1:
                            freq = parts[1].strip().lower().replace("ghz", "")
                            try:
                                cpu["cpu_max_frequency_ghz"] = str(round(float(freq), 2))
                            except ValueError:
                                pass
                        break
        else:
            try:
                result = subprocess.run(["dmidecode", "-t", "processor"], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    for line in result.stdout.splitlines():
                        if "Max Speed" in line:
                            freq = line.split(":")[1].strip().lower().replace("mhz", "")
                            try:
                                cpu["cpu_max_frequency_ghz"] = str(round(int(freq) / 1000, 2))
                            except ValueError:
                                pass
                            break
            except (subprocess.SubprocessError, FileNotFoundError):
                pass
    except Exception:
        pass
    return cpu

def get_memory_info():
    mem = {"memory_total_mb": "unknown", "memory_free_mb": "unknown"}
    try:
        # Memory size
        if os.path.exists("/proc/meminfo"):
            with open("/proc/meminfo", "r") as f:
                lines = f.readlines()
                total = next((line for line in lines if line.startswith("MemTotal")), None)
                free = next((line for line in lines if line.startswith("MemAvailable")), None)
                if total:
                    mem["memory_total_mb"] = str(int(total.split()[1]) // 1024)
                if free:
                    mem["memory_free_mb"] = str(int(free.split()[1]) // 1024)
        # Memory speed detection
        system = platform.system().lower()
        if system == "linux":
            # dmidecode
            try:
                result = subprocess.run(["dmidecode", "-t", "memory"], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    for line in result.stdout.splitlines():
                        if "Speed" in line and "MHz" in line and "Unknown" not in line and "Configured" not in line:
                            speed = line.split(":")[1].strip().lower().replace("mhz", "").strip()
                            try:
                                mem["memory_speed_mhz"] = str(int(speed))
                                return mem
                            except ValueError:
                                pass
            except (subprocess.SubprocessError, FileNotFoundError):
                pass
            # hwinfo
            try:
                result = subprocess.run(["hwinfo", "--memory"], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    for line in result.stdout.splitlines():
                        if "Speed" in line and "MHz" in line:
                            speed = line.split(":")[1].strip().lower().replace("mhz", "").strip()
                            try:
                                mem["memory_speed_mhz"] = str(int(speed))
                                return mem
                            except ValueError:
                                pass
            except (subprocess.SubprocessError, FileNotFoundError):
                pass
            # lscpu
            try:
                result = subprocess.run(["lscpu"], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    for line in result.stdout.splitlines():
                        if "Memory speed" in line or "DDR" in line:
                            parts = line.split()
                            for part in parts:
                                if "MHz" in part:
                                    speed = part.replace("MHz", "").strip()
                                    try:
                                        mem["memory_speed_mhz"] = str(int(float(speed)))
                                        return mem
                                    except ValueError:
                                        pass
            except (subprocess.SubprocessError, FileNotFoundError):
                pass
            # /sys/devices
            try:
                for mem_dir in os.listdir("/sys/devices/system/memory"):
                    speed_path = f"/sys/devices/system/memory/{mem_dir}/speed"
                    if os.path.exists(speed_path):
                        with open(speed_path, "r") as f:
                            speed = f.read().strip()
                            try:
                                mem["memory_speed_mhz"] = str(int(speed))
                                return mem
                            except ValueError:
                                pass
            except Exception:
                pass
        elif system == "windows":
            # wmic
            try:
                result = subprocess.run(["wmic", "memorychip", "get", "Speed"], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    lines = result.stdout.strip().splitlines()
                    for line in lines[1:]:
                        speed = line.strip()
                        if speed and speed.isdigit():
                            mem["memory_speed_mhz"] = speed
                            return mem
            except (subprocess.SubprocessError, FileNotFoundError):
                pass
            # PowerShell
            try:
                result = subprocess.run(["powershell", "-Command", "Get-CimInstance Win32_PhysicalMemory | Select-Object -ExpandProperty Speed"], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    speed = result.stdout.strip()
                    if speed and speed.isdigit():
                        mem["memory_speed_mhz"] = speed
                        return mem
            except (subprocess.SubprocessError, FileNotFoundError):
                pass
        elif system == "darwin":
            # system_profiler
            try:
                result = subprocess.run(["system_profiler", "SPMemoryDataType"], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    for line in result.stdout.splitlines():
                        if "Speed" in line and "MHz" in line:
                            speed = line.split(":")[1].strip().lower().replace("mhz", "").strip()
                            try:
                                mem["memory_speed_mhz"] = str(int(speed))
                                return mem
                            except ValueError:
                                pass
            except (subprocess.SubprocessError, FileNotFoundError):
                pass
            # ioreg
            try:
                result = subprocess.run(["ioreg", "-l"], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    for line in result.stdout.splitlines():
                        if "DIMM Speed" in line:
                            speed = line.split("=")[1].strip().lower().replace("mhz", "").strip()
                            try:
                                mem["memory_speed_mhz"] = str(int(speed))
                                return mem
                            except ValueError:
                                pass
            except (subprocess.SubprocessError, FileNotFoundError):
                pass
    except Exception:
        pass
    return mem

def get_disk_info():
    disks = {}
    try:
        result = subprocess.run(["lsblk", "--json", "-b", "-o", "NAME,MODEL,SIZE,MOUNTPOINTS,TYPE"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            blockdevices = data.get("blockdevices", [])
            nvme_devices = [d for d in blockdevices if d.get("name", "").startswith("nvme")]
            for i, device in enumerate(nvme_devices):
                name = device.get("name", "unknown")
                model = device.get("model", "unknown").strip() or "unknown"
                size_bytes = int(device.get("size", 0))
                total_gb = str(size_bytes // (1024 ** 3))
                disk_type = "SSD"
                try:
                    rotational_file = f"/sys/block/{name}/queue/rotational"
                    if os.path.exists(rotational_file):
                        with open(rotational_file, "r") as f:
                            rotational = f.read().strip()
                            disk_type = "HDD" if rotational == "1" else "SSD"
                except Exception:
                    pass
                if "SSD" in model.upper() or device.get("type", "").lower() == "nvme":
                    disk_type = "SSD"
                mountpoints = device.get("mountpoints", [])
                free_gb = "unknown"
                for mp in mountpoints:
                    if mp:
                        try:
                            stat = os.statvfs(mp)
                            free_gb = str((stat.f_bavail * stat.f_frsize) // (1024 ** 3))
                            break
                        except Exception:
                            continue
                if free_gb == "unknown":
                    for mp in ["/", "/home", "/data", "/mnt"]:
                        try:
                            if os.path.exists(mp):
                                stat = os.statvfs(mp)
                                free_gb = str((stat.f_bavail * stat.f_frsize) // (1024 ** 3))
                                break
                        except Exception:
                            continue
                disks.update({
                    f"disk_{i}_name": name,
                    f"disk_{i}_model": model,
                    f"disk_{i}_total_gb": total_gb,
                    f"disk_{i}_free_gb": free_gb,
                    f"disk_{i}_type": disk_type
                })
    except (subprocess.SubprocessError, FileNotFoundError, json.JSONDecodeError):
        pass
    if not disks:
        disks = {"disk_0_name": "unknown", "disk_0_model": "unknown", "disk_0_total_gb": "unknown", "disk_0_free_gb": "unknown", "disk_0_type": "unknown"}
    return disks

def get_gpu_info():
    try:
        result = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            if lines:
                name, vram, driver = lines[0].split(", ")
                vram_mb = str(int(vram.split()[0]))
                return {"gpu_brand": "NVIDIA", "gpu_name": name, "gpu_vram_mb": vram_mb, "gpu_driver_version": driver}
    except (subprocess.SubprocessError, FileNotFoundError):
        pass
    try:
        result = subprocess.run(["rocm-smi", "--showmeminfo", "vram", "--showdriverversion", "--json"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            for gpu_id, gpu_data in data.items():
                vram_mb = str(gpu_data.get("VRAM", {}).get("Total", 0) // (1024 * 1024))
                driver = str(gpu_data.get("Driver Version", "unknown"))
                return {"gpu_brand": "AMD", "gpu_name": gpu_id, "gpu_vram_mb": vram_mb, "gpu_driver_version": driver}
    except (subprocess.SubprocessError, FileNotFoundError, json.JSONDecodeError):
        pass
    return {"gpu_brand": "none", "gpu_name": "unknown", "gpu_vram_mb": "0", "gpu_driver_version": "unknown"}

def get_os_info():
    os_info = {"system": str(platform.system()), "release": str(platform.release()), "os_distribution": "unknown"}
    try:
        result = subprocess.run(["lsb_release", "-ds"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            os_info["os_distribution"] = result.stdout.strip()
    except (subprocess.SubprocessError, FileNotFoundError):
        try:
            with open("/etc/os-release", "r") as f:
                for line in f:
                    if line.startswith("PRETTY_NAME"):
                        os_info["os_distribution"] = line.split("=")[1].strip().strip('"')
                        break
        except Exception:
            pass
    return os_info

def main():
    profile = {}
    profile.update(get_cpu_info())
    profile.update(get_memory_info())
    profile.update(get_disk_info())
    profile.update(get_gpu_info())
    profile.update(get_os_info())
    print(json.dumps(profile))

if __name__ == "__main__":
    main()
