import platform as sys_platform

def get_platform_specific_module():
    current_platform = sys_platform.system()
    if current_platform == "Windows":
        from platform.windows import WindowsPlatform
        return WindowsPlatform()
    else:
        from platform.linux import LinuxPlatform
        return LinuxPlatform()