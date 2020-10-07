#
# PyArchLinux Installer 0.5
# by odziom91
#

# imports
import os as o
import subprocess as s
import time as t

# colors
# Regular Colors
black = '\033[0;30m'        # Black
red = '\033[0;31m'          # Red
green = '\033[0;32m'        # Green
yellow = '\033[0;33m'       # Yellow
blue = '\033[0;34m'         # Blue
purple = '\033[0;35m'       # Purple
cyan = '\033[0;36m'         # Cyan
white = '\033[0;37m'        # White

# vars
keymap = "not choosed"
locale = "not choosed"
locale2 = "not choosed"
timezone = "not choosed"
nm = "nmcli"
multilib = "no"
dhcp = "yes"
desktop_env = "not choosed"
desktop_mngr = "not choosed"
hostname = ""
root_pwd_status = "not set"
root_pwd = ""
wifi_support = "no"
pppoe_support = "no"
mobile_support = "no"
video_driver = "not choosed"
users_list = []
users_passwd = []


def clear():  # clear screen function
    o.system("clear")

def separator():
    print('-' * 77)

def version():
    version = "0.5"
    print(' ' * 39 + 'version ' + version)

def arch_logo():  # PyArchLinux Installer ASCII logo
    print('%s' % cyan)
    print(r'                                                                             ')
    print(r'        .                                                                    ')
    print(r'       / \                                                                   ')
    print(r'      /   \        ___          _             _     _     _                  ')
    print(r'     /^.   \      | _ \ _  _   /_\   _ _  __ | |_  | |   (_) _ _  _  _ __ __ ')
    print(r'    /  .-.  \     |  _/| || | / _ \ | ._|/ _|| . \ | |__ | || . \| || |\ \ / ')
    print(r'   /  (   ) _\    |_|   \_, |/_/ \_\|_|  \__||_||_||____||_||_||_|\_,_|/_\_\ ')
    print(r'  / _.~   ~._^\         |__/                                                 ')
    print(r' /.^         ^.\                                                             ')
    separator()
    version()
    separator()
    print('%s' % white)


def arch_runcmd(cmd):  # Running commands
    s.call(cmd, shell=True)


def arch_disk_management(efi):  # Disk management menu
    if efi == 1:
        uefi = "YES"
    else:
        uefi = "NO "
    retry = 1
    while retry == 1:
        clear()
        arch_logo()
        separator()
        print("  Disk Management - menu - UEFI mode: " + uefi)
        separator()
        print("")
        print("Note:")
        print("Boot partitions should be prepared on disk with CORRECT disk table!")
        print("For UEFI mode - GPT table")
        print("For BIOS/Legacy mode - MSDOS table")
        print("")
        print(" Choose action:")
        print(" 1. Check disk table")
        separator()
        print(" Use below options with CAUTION! - may destroy your data!")
        print(" 2. Change partition table")
        print(" 3. Create partition")
        print(" 4. Format partition")
        separator()
        print(" 5. Mount partition")
        print(" 0. Exit")
        print(" Your choice?")
        choice = input()
        if choice != "0":
            if choice == "1":
                arch_check_tables(efi)
            if choice == "2":
                arch_change_table(efi)
            if choice == "3":
                arch_partitioning(efi)
            if choice == "4":
                arch_formatting(efi)
            if choice == "5":
                arch_mounting(efi)
        else:
            retry = 0


def arch_check_tables(efi):  # Check MBR (MSDOS) and GPT tables
    if efi == 1:
        uefi = "YES"
    else:
        uefi = "NO "
    retry = 1
    while retry == 1:
        clear()
        arch_logo()
        separator()
        print("  Disk Management - check tables - UEFI mode: " + uefi)
        separator()
        print(" Check list below:")
        get = s.check_output("parted -l", shell=True).decode("utf-8").splitlines()
        for line in get:
            if "Disk /" in line:
                print("")
                print(line)
            if "Partition Table" in line:
                print(line)
                print("")
        print("")
        print("Note:")
        print("Boot partitions should be prepared on disk with CORRECT disk")
        print("table.")
        print("For UEFI mode - GPT table")
        print("For BIOS/Legacy mode - MSDOS table")
        print("")
        print("Press enter to continue")
        e = input()
        print(e)
        retry = 0


def arch_change_table(efi):  # Change disk table - MBR or GPT
    if efi == 1:
        uefi = "YES"
    else:
        uefi = "NO "
    retry = 1
    while retry == 1:
        clear()
        arch_logo()
        separator()
        print("  Disk Management - change partition table - UEFI mode: " + uefi)
        separator()
        print(" Select disk for change partition table:")
        get = s.check_output("parted -l", shell=True).decode("utf-8").splitlines()
        for line in get:
            if "Disk /" in line:
                print("")
                print(line)
            if "Partition Table" in line:
                print(line)
                print("")
        print("Your choice [examples sda, sdb, hda, hdb, etc.]:")
        disk = input()
        print("Your choice is /dev/" + disk)
        print("Are you sure? [y/n]")
        choice1 = input()
        if choice1 == "y":
            print("Choose partition type:")
            print("1. GPT [UEFI MODE]")
            print("2. MSDOS [LEGACY/BIOS MODE]")
            print("Your choice?")
            table = input()
            print("This action will DESTROY your data!")
            print("Are you sure? [y/n]")
            choice2 = input()
            if choice2 == "y":
                if table == "1":
                    arch_runcmd("parted -s /dev/" + disk + " mklabel gpt")
                if table == "2":
                    arch_runcmd("parted -s /dev/" + disk + " mklabel msdos")
                print("Done.")
                t.sleep(3)
                retry = 0
            else:
                retry = 0
        else:
            retry = 0


def arch_partitioning(efi):  # Disk management - Create partition
    if efi == 1:
        uefi = "YES"
    else:
        uefi = "NO "
    retry = 1
    while retry == 1:
        clear()
        arch_logo()
        disk_table = []
        disk_size = []
        separator()
        print("  Disk Management - create partition - UEFI mode: " + uefi)
        separator()
        print(" Select disk for preparing partitions")
        list_disk = s.check_output("lsblk", shell=True).decode("utf-8").splitlines()
        for line in list_disk:
            if "disk" in line:
                lsplit = line.split()
                disk_table.append(lsplit[0])
                disk_size.append(lsplit[3])
        i = 0
        for disk in disk_table:
            print(str(i + 1) + ".\t" + disk + "\t--\t" + disk_size[i])
            i += 1
        print("q.\tQuit\n\nYour choice?")
        get = input()
        if get != "q":
            if int(get) - 1 < len(disk_table):
                print("Your choice is /dev/" + disk_table[int(get) - 1])
                print("Are you sure? [y/n]")
                choice1 = input()
                if choice1 == "y":
                    arch_runcmd("cfdisk /dev/" + disk_table[int(get) - 1])
                    o.system("clear")
                    arch_logo()
                    separator()
                    print("  Disk Management - UEFI mode: " + uefi)
                    separator()
                    print(" Select other disk? [y/n]")
                    choice2 = input()
                    if choice2 == "y":
                        retry = 1
                    else:
                        retry = 0
                else:
                    retry = 1
            else:
                retry = 1
        else:
            retry = 0


def arch_formatting(efi):  # Disk management - Format partition
    if efi == 1:
        uefi = "YES"
    else:
        uefi = "NO "
    retry = 1
    while retry == 1:
        clear()
        arch_logo()
        part_table = []
        part_size = []
        part_type = []
        separator()
        print("  Partition Management - format partition - UEFI mode: " + uefi)
        separator()
        print(" Select partition for formatting")
        list_disk = s.check_output("lsblk -o NAME,SIZE,FSTYPE,TYPE", shell=True).decode("utf-8").splitlines()
        for line in list_disk:
            if "part" in line:
                lsplit = line.split()
                part_table.append(lsplit[0])
                part_size.append(lsplit[1])
                part_type.append(lsplit[2])
        i = 0
        for part in part_table:
            print(str(i + 1) + ".\t" + part + " -- " + part_size[i] + " -- " + part_type[i])
            i += 1
        print("q.\tQuit\n\nYour choice?")
        get = input()
        if get != "q":
            if int(get) - 1 < len(part_table):
                print("Select partition type:")
                print("1. ext4")
                print("2. fat32")
                print("3. swap")
                print("4. btrfs (unstable)")
                print()
                print("--- NOTE! ---")
                print("Btrfs has some features that are unstable.")
                print("If you have btrfs filesystems, run the latest kernel.")
                print("You should keep and test backups of your data, and be prepared to use them.")
                print("Known issues: no build-in encryption, btrfs check, TLP and file corruptions.")
                print()
                print("q. Quit")
                print("")
                print("Your choice?")
                get_fs = input()
                if get_fs != "q":
                    print("Partition: /dev/" + part_table[int(get) - 1].lstrip("└─").lstrip("├─"))
                    if get_fs == "1":
                        print("File system: ext4")
                    if get_fs == "2":
                        print("File system: fat32")
                    if get_fs == "3":
                        print("File system: swap")
                    if get_fs == "4":
                        print("File system: btrfs")
                    print("Are you sure? [y/n]")
                    choice = input()
                    if choice == "y":
                        if get_fs == "1":
                            arch_runcmd("mkfs.ext4 /dev/" + part_table[int(get) - 1].lstrip("└─").lstrip("├─"))
                        if get_fs == "2":
                            arch_runcmd("mkfs.fat -F32 /dev/" + part_table[int(get) - 1].lstrip("└─").lstrip("├─"))
                        if get_fs == "3":
                            arch_runcmd("mkswap /dev/" + part_table[int(get) - 1].lstrip("└─").lstrip("├─"))
                        if get_fs == "4":
                            arch_runcmd("mkfs.btrfs -f /dev/" + part_table[int(get) - 1].lstrip("└─").lstrip("├─"))
                        print(" Select other partition? [y/n]")
                        choice2 = input()
                        if choice2 == "y":
                            retry = 1
                        else:
                            retry = 0
                    else:
                        retry = 1
                else:
                    retry = 0
            else:
                retry = 1
        else:
            retry = 0


def arch_mounting(efi):  # Disk management - Mount partition
    if efi == 1:
        uefi = "YES"
    else:
        uefi = "NO "
    retry = 1
    while retry == 1:
        clear()
        arch_logo()
        part_table = []
        part_size = []
        part_type = []
        part_mount = []
        separator()
        print("  Mount file systems - mount partition - UEFI mode: " + uefi)
        separator()
        print("Select partition for mount")
        list_disk = s.check_output("lsblk -o NAME,SIZE,FSTYPE,TYPE,MOUNTPOINT", shell=True).decode("utf-8").splitlines()
        for line in list_disk:
            if "part" in line:
                lsplit = line.split()
                part_table.append(lsplit[0])
                part_size.append(lsplit[1])
                part_type.append(lsplit[2])
                try:
                    part_mount.append(lsplit[4])
                except Exception as e:
                    print(e)
                    part_mount.append("not mounted")
        i = 0
        for part in part_table:
            print(str(i + 1) + ".\t" + part + " -- " + part_size[i] + " -- " + part_type[i] + " -- " + part_mount[i])
            i += 1
        print("q.\tQuit\n\nYour choice?")
        get = input()
        if get != "q":
            if int(get) - 1 < len(part_table):
                print("Select mount point:")
                print("1. / - must be mounted at first!")
                print("2. /boot")
                print("3. /boot/efi - required if UEFI mode is ON!")
                print("4. /home")
                print("5. swap")
                print("6. other mount point")
                print("q. Cancel")
                mnt = input()
                if mnt != "q":
                    if mnt == "1":
                        arch_runcmd("umount /mnt")
                        arch_runcmd("mount /dev/" + part_table[int(get) - 1].lstrip("└─").lstrip("├─") + " /mnt")
                    if mnt == "2":
                        arch_runcmd("mkdir -p /mnt/boot")
                        arch_runcmd("umount /mnt/boot")
                        arch_runcmd("mount /dev/" + part_table[int(get) - 1].lstrip("└─").lstrip("├─") + " /mnt/boot")
                    if mnt == "3":
                        arch_runcmd("mkdir -p /mnt/boot/efi")
                        arch_runcmd("umount /mnt/boot/efi")
                        arch_runcmd("mount /dev/" + part_table[int(get) - 1].lstrip("└─").lstrip("├─") +
                                    " /mnt/boot/efi")
                    if mnt == "4":
                        arch_runcmd("mkdir -p /mnt/home")
                        arch_runcmd("umount /mnt/home")
                        arch_runcmd("mount /dev/" + part_table[int(get) - 1].lstrip("└─").lstrip("├─") + " /mnt/home")
                    if mnt == "5":
                        arch_runcmd("swapon /dev/" + part_table[int(get) - 1].lstrip("└─").lstrip("├─"))
                    if mnt == "6":
                        print("Sorry! :( This option is not implemented yet!")
                    print(" Select other mount point? [y/n]")
                    choice2 = input()
                    if choice2 == "y":
                        retry = 1
                    else:
                        retry = 0
                else:
                    retry = 0
        else:
            retry = 0


def arch_bootloader(efi):  # Install GRUB bootloader via chroot and generated bash script
    retry = 1
    while retry == 1:
        clear()
        arch_logo()
        separator()
        print("  Install GRUB Bootloader ")
        separator()
        print("Are you sure to install GRUB bootloader? [y/n]")
        bootloader = input()
        if bootloader == "y":
            arch_runcmd("rm setup_bootloader.sh")
            arch_runcmd("rm /mnt/setup_bootloader.sh")
            setup = open("setup_bootloader.sh", "a")
            setup.write("#!/bin/bash\n")
            if efi == 1:
                print("EFI mode: YES\n")
                setup.write("pacman -Syy --noconfirm grub efibootmgr os-prober\n")
                setup.write("grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=GRUB\n")
            else:
                print("EFI mode: NO\n")
                print("Select disk to initialize grub:")
                arch_runcmd("lsblk")
                print("Your choice? (sdX or hdX):")
                grub = input()
                setup.write("pacman -Syy --noconfirm grub os-prober\n")
                setup.write("mkdir -p /boot/grub/\n")
                setup.write("grub-install --target=i386-pc /dev/" + grub + "\n")
            setup.write("grub-mkconfig -o /boot/grub/grub.cfg\n")
            setup.write("exit\n")
            setup.close()
            arch_runcmd("cp setup_bootloader.sh /mnt/setup_bootloader.sh")
            arch_runcmd("chmod +x /mnt/setup_bootloader.sh")
            arch_runcmd("arch-chroot /mnt bash -c \"./setup_bootloader.sh\"")
            arch_runcmd("rm /mnt/setup_bootloader.sh")
            retry = 0
        else:
            retry = 0


def arch_iptest():
    clear()
    arch_logo()
    separator()
    print("  Check Internet connection")
    separator()
    print("IP Configuration:")
    arch_runcmd('ip addr | grep -w inet | sed "s/inet/> inet/"')
    print("Pinging archlinux.org. Please wait...")
    #arch_runcmd("ping -c 10 archlinux.org")
    status, request = s.getstatusoutput("ping -c 5 archlinux.org")
    if status == 0:
        print("You have a connection.")
    else:
        print("You do not have a connection.\nPlease check and configure your network card and try again.")
    t.sleep(5)


def arch_locale():
    global locale
    global locale2
    menu = True
    while menu:
        clear()
        arch_logo()
        separator()
        print("  Install Arch Linux - System configuration - Set locale")
        separator()
        #list_locales = s.check_output("localectl list-locales", shell=True).decode("utf-8").splitlines()
        list_locales = ["en_US.UTF-8",
                        "de_DE.UTF-8",
                        "el_GR.UTF-8",
                        "hu.UTF-8",
                        "es_ES.UTF-8",
                        "fr_FR.UTF-8",
                        "it_IT.UTF-8",
                        "pl_PL.UTF-8",
                        "ro_RO.UTF-8",
                        "ru_RU.UTF-8",
                        "sv_SE.UTF-8",
                        "en_GB.UTF-8"]
        print("1.  us - United States")
        print("2.  de - German")
        print("3.  el - Greek")
        print("4.  hu - Hungarian")
        print("5.  es - Spanish")
        print("6.  fr - French")
        print("7.  it - Italian")
        print("8.  pl - Polish")
        print("9.  ro - Romanian")
        print("10. ru - Russian")
        print("11. sv - Swedish")
        print("12. uk - United Kingdom")
        '''
        i = 0
        for lc in list_locales:
            i += 1
            if (i % 4) == 0:
                print(str(i) + ". " + lc + "\n")
            else:
                print(str(i) + ". " + lc + "\t")
        '''
        print("q. Quit")
        try:
            choice = input("Choose locale from list: ")
            if choice != "q":
                x = int(choice)
                locale = list_locales[x-1]
                spl_locale = locale.split(".")
                locale2 = locale + " " + spl_locale[1]
                config = open("./config/locale.conf", "w")
                config.write(locale + "\n")
                config.write(locale2)
                config.close()
                menu = False
            else:
                menu = False
        except ValueError:
            print("Wrong value!")
            menu = False
            t.sleep(3)
        except IndexError:
            print("Wrong value!")
            menu = False
            t.sleep(3)


def arch_keymap():
    global keymap
    menu = True
    while menu:
        clear()
        arch_logo()
        separator()
        print("  Install Arch Linux - System configuration - Set keymap")
        separator()
        print("Choose keyboard layout:")
        print("1.  us - United States")
        print("2.  de - German")
        print("3.  el - Greek")
        print("4.  hu - Hungarian")
        print("5.  es - Spanish")
        print("6.  fr - French")
        print("7.  it - Italian")
        print("8.  pl - Polish")
        print("9.  ro - Romanian")
        print("10. ru - Russian")
        print("11. sv - Swedish")
        print("12. uk - United Kingdom")
        print("13. Choose other keyboard layout")
        print("q.  Quit")
        print()
        choice = input("Select option from list: ")
        if choice != "q":
            if choice == "1":
                keymap = "us"
                menu = False
            if choice == "2":
                keymap = "de"
                menu = False
            if choice == "3":
                keymap = "el"
                menu = False
            if choice == "4":
                keymap = "hu"
                menu = False
            if choice == "5":
                keymap = "es"
                menu = False
            if choice == "6":
                keymap = "fr"
                menu = False
            if choice == "7":
                keymap = "it"
                menu = False
            if choice == "8":
                keymap = "pl"
                menu = False
            if choice == "9":
                keymap = "ro"
                menu = False
            if choice == "10":
                keymap = "ru"
                menu = False
            if choice == "11":
                keymap = "sv"
                menu = False
            if choice == "12":
                keymap = "uk"
                menu = False
            if choice == "13":
                clear()
                arch_logo()
                separator()
                print("  Install Arch Linux - System configuration - Set keymap - other")
                separator()
                filter = input("Put COUNTRY CODE or other keyboard type for filter: ")
                list_keymaps = s.check_output("localectl list-keymaps | grep \"" + filter + "\"", shell=True).decode("utf-8").split("\n")
                i = 0
                for km in list_keymaps:
                    i += 1
                    if km != "":
                        if (i % 4) == 0:
                            print(str(i) + ". " + km, end='\n')
                        else:
                            print(str(i) + ". " + km, end='\n')
                print("q. Quit")
                try:
                    choice = input("Choose keymap from list: ")
                    if choice != "q":
                        x = int(choice)
                        keymap = list_keymaps[x - 1]
                        menu = False
                    else:
                        menu = False
                except ValueError:
                    print("Wrong value!")
                    menu = False
                    t.sleep(3)
                except IndexError:
                    print("Wrong value!")
                    menu = False
                    t.sleep(3)
            config = open("./config/keymap.conf", "w")
            config.write(keymap)
            config.close()
        else:
            menu = False


def arch_timezone():
    global timezone
    menu = True
    while menu:
        clear()
        arch_logo()
        separator()
        print("  Install Arch Linux - System configuration - Set time zone")
        separator()
        print("Choose place:")
        list_tz = s.check_output("timedatectl list-timezones", shell=True).decode("utf-8").split("\n")
        list_tz_1 = []
        for v_tz in list_tz:
            value = v_tz.split("/")
            list_tz_1.append(value[0])
        list_tz_1 = list(dict.fromkeys(list_tz_1))
        i = 0
        for v_tz_1 in list_tz_1:
            if v_tz_1 != "":
                i += 1
                print(str(i) + ". " + v_tz_1)
        print("l. Set localtime")
        print("q. Quit")
        choice = input("Choose an option: ")
        if choice != "q":
            if choice == "l":
                print("Sorry, option not supported.")
            else:
                try:
                    x = int(choice)
                    list_tz = s.check_output("timedatectl list-timezones | grep \"" + list_tz_1[x - 1] + "\"", shell=True).decode("utf-8").split("\n")
                    i = 0
                    clear()
                    arch_logo()
                    print("Choose nearest city: ")
                    for v_tz in list_tz:
                        if v_tz != "":
                            tz_city = v_tz.split("/")
                            i += 1
                            if i % 3 == 0:
                                print(str(i) + ". " + tz_city[1], end="\n")
                            else:
                                print(str(i) + ". " + tz_city[1], end="\t")
                    print("q. Quit")
                    choice = input("Choose an option: ")
                    if choice != "q":
                        x = int(choice)
                        timezone = list_tz[x - 1]
                        config = open("./config/timezone.conf", "w")
                        config.write(timezone)
                        config.close()
                        menu = False
                    else:
                        menu = False
                except ValueError:
                    print("Wrong value!")
                    menu = False
                    t.sleep(3)
                except IndexError:
                    print("Wrong value!")
                    menu = False
                    t.sleep(3)
        else:
            menu = False


def arch_network():
    global nm
    menu = True
    while menu:
        clear()
        arch_logo()
        separator()
        print("  Install Arch Linux - System configuration - Set Network Manager")
        separator()
        print(" 1.  networkmanager - for Graphical User Interface (nmcli)")
        print(" 2.  netctl - netctl Network Utility (wifi-menu)")
        print(" q.  Quit")
        print("")
        choice = input("Choose an option: ")
        if choice != "q":
            if choice == "1":
                nm = "nmcli"
                menu = False
            if choice == "2":
                nm = "wifi-menu"
                menu = False
            config = open("./config/network.conf", "w")
            config.write(nm)
            config.close()
        else:
            menu = False


def arch_multilib():
    global multilib
    menu = True
    while menu:
        clear()
        arch_logo()
        separator()
        print("  Install Arch Linux - System configuration - Multilib")
        separator()
        print("Enable multilib? Required for 32-bit support")
        print("y. Yes")
        print("n. No")
        choice = input("Choose your answer: ")
        if choice == "y":
            multilib = "yes"
            config = open("./config/multilib.conf", "w")
            config.write(multilib)
            config.close()
        if choice == "n":
            multilib = "no"
            config = open("./config/multilib.conf", "w")
            config.write(multilib)
            config.close()
        menu = False


def arch_dhcp():
    global dhcp
    menu = True
    while menu:
        clear()
        arch_logo()
        separator()
        print("  Install Arch Linux - System configuration - Enable DHCP")
        separator()
        print("Enable DHCP? It is required for automatic IP address configuration")
        print("y. Yes")
        print("n. No")
        choice = input("Choose your answer: ")
        if choice == "y":
            dhcp = "yes"
            config = open("./config/dhcp.conf", "w")
            config.write(dhcp)
            config.close()
        if choice == "n":
            config = open("./config/dhcp.conf", "w")
            config.write(dhcp)
            config.close()
            dhcp = "no"
        menu = False


def arch_wifi():
    global wifi_support
    menu = True
    while menu:
        clear()
        arch_logo()
        separator()
        print("  Install Arch Linux - System configuration - Enable Wi-Fi")
        separator()
        print("Enable Wi-Fi support?")
        print("y. Yes")
        print("n. No")
        choice = input("Choose your answer: ")
        if choice == "y":
            wifi_support = "yes"
            config = open("./config/wifi.conf", "w")
            config.write(wifi_support)
            config.close()
        if choice == "n":
            wifi_support = "no"
            config = open("./config/wifi.conf", "w")
            config.write(wifi_support)
            config.close()
        menu = False


def arch_pppoe():
    global pppoe_support
    menu = True
    while menu:
        clear()
        arch_logo()
        separator()
        print("  Install Arch Linux - System configuration - Enable PPPoE")
        separator()
        print("Enable PPPoE support?")
        print("y. Yes")
        print("n. No")
        choice = input("Choose your answer: ")
        if choice == "y":
            pppoe_support = "yes"
            config = open("./config/pppoe.conf", "w")
            config.write(pppoe_support)
            config.close()
        if choice == "n":
            pppoe_support = "no"
            config = open("./config/pppoe.conf", "w")
            config.write(pppoe_support)
            config.close()
        menu = False


def arch_mobile():
    global mobile_support
    menu = True
    while menu:
        clear()
        arch_logo()
        separator()
        print("  Install Arch Linux - System configuration - Enable mobile")
        separator()
        print("Enable mobile connection support?")
        print("y. Yes")
        print("n. No")
        choice = input("Choose your answer: ")
        if choice == "y":
            mobile_support = "yes"
            config = open("./config/mobile.conf", "w")
            config.write(mobile_support)
            config.close()
        if choice == "n":
            mobile_support = "no"
            config = open("./config/mobile.conf", "w")
            config.write(mobile_support)
            config.close()
        menu = False


def arch_usermgmt():
    menu = True
    while menu:
        clear()
        arch_logo()
        separator()
        print("  Install Arch Linux - Install menu ")
        separator()
        print(" Users list:")
        for user in users_list:
            print(user)
        print()
        print(" a. Add user")
        #print(" e. Edit user")
        print(" d. Delete user")
        print(" q. Quit")
        choice = input("Choose an option: ")
        if choice != "q":
            if choice == "a":
                username = input("New username: ")
                if username != "" and username != "root":
                    users_list.append(username)
                    config = open("./config/users.conf", "w")
                    for user in users_list:
                        config.write(user + "\n")
                    config.close()
            '''if choice == "e":
                i = 0
                for user in users_list:
                    i += 1
                    print(str(i) + ". " + user)
                try:
                    choice = input("Choose an option: ")
                    if choice != "q":
                        print("Editing " + users_list[int(choice) - 1])
                        user_passwd = input("Password: ")
                        users_passwd[int(choice) - 1] = user_passwd
                except ValueError:
                    print("Wrong value!")
                    t.sleep(3)
                except IndexError:
                    print("Wrong value!")
                    t.sleep(3)
            '''
            if choice == "d":
                i = 0
                for user in users_list:
                    i += 1
                    print(str(i) + ". " + user)
                try:
                    choice = input("Choose an option: ")
                    if choice != "q":
                        users_list.remove(users_list[int(choice) - 1])
                        config = open("./config/users.conf", "w")
                        for user in users_list:
                            config.write(user + "\n")
                        config.close()
                except ValueError:
                    print("Wrong value!")
                    t.sleep(3)
                except IndexError:
                    print("Wrong value!")
                    t.sleep(3)
        else:
            menu = False


def arch_desktop_env():
    global desktop_env
    menu = True
    while menu:
        clear()
        arch_logo()
        separator()
        print("  Install Arch Linux - System configuration - Choose Desktop Environment")
        separator()
        print("Choose desktop environment:")
        print("1. Gnome")
        print("2. KDE Plasma")
        print("3. Mate")
        print("4. Xfce")
        print("5. Cinnamon")
        # todo
        #print("6. Budgie")
        #print("7. Deepin")
        #print("8. Enlightenment")
        #print("9. LXDE")
        #print("10. LQxt")
        print("q. Quit")
        choice = input("Choose an option: ")
        if choice != "q":
            if choice == "1":
                desktop_env = "gnome"
                menu = False
            if choice == "2":
                desktop_env = "kde"
                menu = False
            if choice == "3":
                desktop_env = "mate"
                menu = False
            if choice == "4":
                desktop_env = "xfce4"
                menu = False
            if choice == "5":
                desktop_env = "cinnamon"
                menu = False
            config = open("./config/de.conf", "w")
            config.write(desktop_env)
            config.close()
        else:
            menu = False


def arch_video():
    global video_driver
    menu = True
    while menu:
        clear()
        arch_logo()
        separator()
        print("  Install Arch Linux - System configuration - Choose video driver")
        separator()
        print("Choose video driver:")
        print("1. NVidia")
        print("2. AMD")
        print("3. Intel")
        print("4. VirtualBox")
        print("q. Quit")
        choice = input("Choose an option: ")
        if choice != "q":
            if choice == "1":
                video_driver = "nvidia"
                menu = False
            if choice == "2":
                video_driver = "amd"
                menu = False
            if choice == "3":
                video_driver = "intel"
                menu = False
            if choice == "4":
                video_driver = "virtualbox"
                menu = False
            config = open("./config/video.conf", "w")
            config.write(video_driver)
            config.close()
        else:
            menu = False


def arch_desktop_mngr():
    global desktop_mngr
    menu = True
    while menu:
        clear()
        arch_logo()
        separator()
        print("  Install Arch Linux - System configuration - Choose Display Manager ")
        separator()
        print("Choose desktop environment:")
        print("1. gdm - GNOME Desktop Display Manager")
        print("2. lightdm - Multi Desktop Display Manager")
        # todo
        # other display managers
        print("q. Quit")
        choice = input("Choose an option: ")
        if choice != "q":
            if choice == "1":
                desktop_mngr = "gdm"
                menu = False
            if choice == "2":
                desktop_mngr = "lightdm"
                menu = False
            config = open("./config/dm.conf", "w")
            config.write(desktop_mngr)
            config.close()
        else:
            menu = False


def arch_hostname():
    global hostname
    menu = True
    while menu:
        clear()
        arch_logo()
        separator()
        print("  Install Arch Linux - System configuration - Set Hostname ")
        separator()
        choice = input("Insert hostname: ")
        if choice != "":
            hostname = choice
            config = open("./config/hostname.conf", "w")
            config.write(hostname)
            config.close()
            menu = False
        else:
            menu = False


def arch_root_pwd():
    global root_pwd_status
    global root_pwd
    menu = True
    while menu:
        clear()
        arch_logo()
        separator()
        print("  Install Arch Linux - System configuration - Set Root password ")
        separator()
        choice = input("Insert password for root: ")
        if choice != "":
            root_pwd_status = "set"
            root_pwd = choice
            menu = False
        else:
            menu = False


def arch_sysconfig(efi):
    global locale
    global keymap
    global timezone
    global nm
    global multilib
    global dhcp
    global desktop_env
    global desktop_mngr
    global hostname
    global root_pwd_status
    global wifi_support
    global pppoe_support
    global mobile_support
    global video_driver
    menu = True
    while menu:
        clear()
        arch_logo()
        separator()
        print("  Install Arch Linux - System configuration")
        separator()
        print(" 1.  Set locale - " + locale + " " + locale2)
        print(" 2.  Set keymap - " + keymap)
        print(" 3.  Set time zone - " + timezone)
        print(" 4.  Set network manager - " + nm)
        print(" 5.  Set Wi-Fi connection - " + wifi_support)
        print(" 6.  Set PPPoE connection - " + pppoe_support)
        print(" 7.  Set Mobile broadband support - " + mobile_support)
        print(" 8.  Enable DHCP (Dynamic Host Control Protocol) - " + dhcp)
        print(" 9.  Choose Desktop Environment - " + desktop_env)
        #print(" 10. Choose Display Manager - " + desktop_mngr)
        print(" 10. Choose video driver - " + video_driver)
        print(" 11. Set Hostname - " + hostname)
        #print(" 13. Set Root password - " + root_pwd_status)
        print(" 12. Users management")
        #print(" 15. Set Administator privileges")
        print(" 13. Choose Multilib (32-bit libraries support) - " + multilib)
        print(" s.  Start configuration !")
        print(" q.  Quit")
        print("")
        choice = input("Choose an option: ")
        if choice != "q":
            if choice == "1":
                arch_locale()
            if choice == "2":
                arch_keymap()
            if choice == "3":
                arch_timezone()
            if choice == "4":
                arch_network()
            if choice == "5":
                arch_wifi()
            if choice == "6":
                arch_pppoe()
            if choice == "7":
                arch_mobile()
            if choice == "8":
                arch_dhcp()
            if choice == "9":
                arch_desktop_env()
            #if choice == "10":
            #    arch_desktop_mngr()
            if choice == "10":
                arch_video()
            if choice == "11":
                arch_hostname()
            #if choice == "13":
            #    arch_root_pwd()
            if choice == "12":
                arch_usermgmt()
            #if choice == "15":
            #    pass
            if choice == "13":
                arch_multilib()
            if choice == "s":
                arch_setup_configuration(efi)
        else:
            menu = False


def arch_software():
    global multilib
    menu = True
    while menu:
        clear()
        arch_logo()
        separator()
        print("  Install Arch Linux - Install additional software ")
        separator()
        print(" 1. Install default software -  check list below:")
        print(" Firefox - internet browser,")
        print(" Thunderbird - mail client,")
        print(" GIMP - graphical editor,")
        print(" LibreOffice - office applications,")
        print(" Audacious - music player,")
        print(" VLC - video player")
        print()
        print(" 2. Install DXVK for gaming! (only for graphic cards with Vulkan!)")
        print(" 3. Install software for gaming!")
        print(" 4. Install software manually")
        print(" q. Quit")
        choice = input("Choose an option: ")
        if choice != "q":
            if choice == "1":
                arch_software_script(["firefox", "thunderbird", "gimp", "libreoffice-fresh", "audacious", "vlc"])
            if choice == "2":
                if multilib == "no":
                    print("Multilib must be enabled!")
                    arch_runcmd("echo \"\" >> /mnt/etc/pacman.conf")
                    arch_runcmd("echo \"[multilib]\" >> /mnt/etc/pacman.conf")
                    arch_runcmd("echo \"Include = /etc/pacman.d/mirrorlist\" >> /mnt/etc/pacman.conf")
                    multilib = "yes"
                if video_driver == "nvidia":
                    arch_software_script(["lib32-nvidia-utils", "vulkan-icd-loader", "lib32-vulkan-icd-loader"])
                if video_driver == "amd":
                    arch_software_script(["lib32-mesa", "vulkan-radeon", "lib32-vulkan-radeon", "vulkan-icd-loader", "lib32-vulkan-icd-loader"])
                if video_driver == "intel":
                    arch_software_script(["lib32-mesa", "vulkan-intel", "lib32-vulkan-intel", "vulkan-icd-loader", "lib32-vulkan-icd-loader"])
                if video_driver == "virtualbox":
                    print("VirtualBox is not supported!")
            if choice == "3":
                if multilib == "no":
                    print("Multilib must be enabled!")
                    arch_runcmd("echo \"\" >> /mnt/etc/pacman.conf")
                    arch_runcmd("echo \"[multilib]\" >> /mnt/etc/pacman.conf")
                    arch_runcmd("echo \"Include = /etc/pacman.d/mirrorlist\" >> /mnt/etc/pacman.conf")
                    multilib = "yes"
                # wine
                arch_software_script(["wine-staging", "giflib", "lib32-giflib", "libpng", "lib32-libpng", "libldap",
                                      "lib32-libldap", "gnutls", "lib32-gnutls", "mpg123", "lib32-mpg123", "openal",
                                      "lib32-openal", "v4l-utils", "lib32-v4l-utils", "libpulse", "lib32-libpulse",
                                      "libgpg-error", "lib32-libgpg-error", "alsa-plugins", "lib32-alsa-plugins",
                                      "alsa-lib", "lib32-alsa-lib", "libjpeg-turbo", "lib32-libjpeg-turbo", "sqlite",
                                      "lib32-sqlite", "libxcomposite", "lib32-libxcomposite", "libxinerama",
                                      "lib32-libgcrypt", "libgcrypt", "lib32-libxinerama", "ncurses", "lib32-ncurses",
                                      "opencl-icd-loader", "lib32-opencl-icd-loader", "libxslt", "lib32-libxslt",
                                      "libva", "lib32-libva", "gtk3", "lib32-gtk3", "gst-plugins-base-libs",
                                      "lib32-gst-plugins-base-libs", "vulkan-icd-loader", "lib32-vulkan-icd-loader"])
                # lutris
                arch_software_script(["lutris"])
                # steam
                arch_software_script(["steam"])
            if choice == "4":
                arch_software_manual()
        else:
            menu = False


def arch_software_script(apps):
    print(">> Clear scripts")
    arch_runcmd("rm setup.sh")
    arch_runcmd("rm /mnt/setup.sh")

    print(">> Prepare scripts")
    setup = open("setup.sh", "a")
    setup.write('#!/bin/bash\n')
    setup.write('clear\n')
    setup.write('echo ">> Installing additional software"\n')
    setup.write('read -t 5 -n 1 -s -r -p "Press wait to continue...\n"\n')
    for app in apps:
        setup.write('pacman -Syy --noconfirm --needed ' + app + '\n')
    setup.write('exit\n')
    setup.close()

    print(">> Prepare to chroot")
    arch_runcmd("cp setup.sh /mnt/setup.sh")
    arch_runcmd("chmod +x /mnt/setup.sh")
    arch_runcmd("cp /etc/pacman.d/mirrorlist /mnt/etc/pacman.d/mirrorlist")

    print(">> Start configuration")
    arch_runcmd("arch-chroot /mnt bash -c \"./setup.sh\"")

    print("Configuration has been completed!")
    arch_runcmd("rm /mnt/setup.sh")


def arch_software_manual():
    arch_runcmd("arch-chroot /mnt")


def arch_setup_menu(efi):
    # todo
    # xf86-input, sudo
    if efi == 1:
        uefi = "YES"
    else:
        uefi = "NO "
    menu = True
    while menu:
        clear()
        arch_logo()
        separator()
        print("  Install Arch Linux - Install menu ")
        separator()
        print(" 1. Install Arch Linux")
        print(" 2. System configuration")
        print(" 3. Install additional software")
        print(" 4. Install bootloader")
        print(" q. Quit")
        choice = input("Choose an option: ")
        if choice != "q":
            if choice == "1":
                arch_setup_kernel(efi)
            if choice == "2":
                arch_sysconfig(efi)
            if choice == "3":
                arch_software()
            if choice == "4":
                arch_bootloader(efi)
        else:
            menu = False


def arch_setup_kernel(efi):
    if efi == 1:
        uefi = "YES"
    else:
        uefi = "NO "
    menu = True
    while menu:
        clear()
        arch_logo()
        separator()
        print("  Install Arch Linux - Choose kernel ")
        separator()
        print(" 1. Stable - Vanilla kernel (default Linux kernel) - linux")
        print(" 2. Zen - Zen kernel (modified kernel - fsync support!) - linux-zen")
        print(" 3. Longterm - Long Time Support kernel - linux-lts")
        print(" 4. Hardened - Security-focused kernel - linux-hardened")
        print(" q. Quit")
        choice = input("Choose an option: ")
        if choice != "q":
            if choice == "1":
                arch_setup_base(efi)
                menu = False
            if choice == "2":
                arch_setup_zen(efi)
                menu = False
            if choice == "3":
                arch_setup_longterm(efi)
                menu = False
            if choice == "4":
                arch_setup_hardened(efi)
                menu = False
        else:
            menu = False


def arch_setup_base(efi):
    if efi == 1:
        uefi = "YES"
    else:
        uefi = "NO "
    retry = True
    while retry:
        clear()
        arch_logo()
        separator()
        print("  Install Arch Linux - Stable - UEFI mode: " + uefi)
        separator()
        print("Please check mount points before continue:")
        arch_runcmd(r'lsblk')
        print("Continue? [y/n]")
        install = input()
        if install == "y":
            print(">> Refresh repositiories")
            arch_runcmd("pacman -Syy")
            print(">> Installing base")
            arch_runcmd("pacstrap /mnt base base-devel linux linux-firmware")
            print(">> Arch Linux base has been installed.")
            t.sleep(5)
            retry = 0
        else:
            retry = 0


def arch_setup_zen(efi):
    if efi == 1:
        uefi = "YES"
    else:
        uefi = "NO "
    retry = True
    while retry:
        clear()
        arch_logo()
        separator()
        print("  Install Arch Linux - Zen - UEFI mode: " + uefi)
        separator()
        print("Please check mount points before continue:")
        arch_runcmd(r'lsblk')
        print("Continue? [y/n]")
        install = input()
        if install == "y":
            print(">> Refresh repositiories")
            arch_runcmd("pacman -Syy")
            print(">> Installing base")
            arch_runcmd("pacstrap /mnt base base-devel linux-zen linux-firmware")
            print(">> Arch Linux base has been installed.")
            t.sleep(5)
            retry = 0
        else:
            retry = 0


def arch_setup_longterm(efi):
    if efi == 1:
        uefi = "YES"
    else:
        uefi = "NO "
    retry = True
    while retry:
        clear()
        arch_logo()
        separator()
        print("  Install Arch Linux - Longterm - UEFI mode: " + uefi)
        separator()
        print("Please check mount points before continue:")
        arch_runcmd(r'lsblk')
        print("Continue? [y/n]")
        install = input()
        if install == "y":
            print(">> Refresh repositiories")
            arch_runcmd("pacman -Syy")
            print(">> Installing base")
            arch_runcmd("pacstrap /mnt base base-devel linux-lts linux-firmware")
            print(">> Arch Linux base has been installed.")
            t.sleep(5)
            retry = 0
        else:
            retry = 0


def arch_setup_hardened(efi):
    if efi == 1:
        uefi = "YES"
    else:
        uefi = "NO "
    retry = True
    while retry:
        clear()
        arch_logo()
        separator()
        print("  Install Arch Linux - Hardened - UEFI mode: " + uefi)
        separator()
        print("Please check mount points before continue:")
        arch_runcmd(r'lsblk')
        print("Continue? [y/n]")
        install = input()
        if install == "y":
            print(">> Refresh repositiories")
            arch_runcmd("pacman -Syy")
            print(">> Installing base")
            arch_runcmd("pacstrap /mnt base base-devel linux-hardened linux-firmware")
            print(">> Arch Linux base has been installed.")
            t.sleep(5)
            retry = 0
        else:
            retry = 0


def arch_setup_configuration(efi):
    global multilib
    global timezone
    global locale
    global locale2
    global keymap
    clear()
    arch_logo()
    separator()
    print("  Install Arch Linux - system configuration ")
    separator()

    print(">> Generate fstab file")
    arch_runcmd("genfstab -U /mnt >> /mnt/etc/fstab")

    print(">> Clear scripts")
    arch_runcmd("rm setup.sh")
    arch_runcmd("rm /mnt/setup.sh")

    print(">> Prepare scripts")
    setup = open("setup.sh", "a")
    setup.write('#!/bin/bash\n')

    setup.write('clear\n')
    setup.write('echo ">> Configuring hostname"\n')
    setup.write('read -t 5 -n 1 -s -r -p "Press wait to continue...\n"\n')
    setup.write('echo ' + hostname + ' > /etc/hostname\n')
    setup.write('echo "> /etc/hosts file"\n')
    setup.write('echo 127.0.0.1 ' + 'localhost' + ' > /etc/hosts\n')
    setup.write('echo ::1 ' + 'localhost' + ' >> /etc/hosts\n')
    setup.write('echo 127.0.1.1 ' + hostname + '.localdomain ' + hostname + ' >> /etc/hosts\n')

    setup.write('clear\n')
    setup.write('echo ">> Configuring root account"\n')
    setup.write('echo "Now you need to setup password for root account."\n')
    setup.write('echo "You need to insert it two times. Password will be not visible!"\n')
    setup.write('read -t 5 -n 1 -s -r -p "Press wait to continue...\n"\n')
    setup.write('passwd\n')

    i = 0
    for user in users_list:
        setup.write('clear\n')
        setup.write('echo ">> Setting ' + user + ' account and password"\n')
        setup.write('groupadd ' + 'users' + '\n')
        setup.write('useradd -m -g ' + 'users' + ' ' + user + '\n')
        setup.write('echo "Please provide a password for user: ' + user + '"\n')
        setup.write('echo "You need to insert it two times. Password will be not visible!"\n')
        setup.write('read -t 5 -n 1 -s -r -p "Press wait to continue...\n"\n')
        setup.write('passwd ' + user + '\n')
        i += 1

    setup.write('clear\n')
    setup.write('echo ">> Configuring time zone"\n')
    setup.write('read -t 5 -n 1 -s -r -p "Press wait to continue...\n"\n')
    setup.write('ln -sf /usr/share/zoneinfo/' + timezone + ' /etc/localtime\n')
    setup.write('timedatectl set-timezone \"' + timezone + '"\n')
    setup.write('echo ">> Configuring system time"\n')
    setup.write('hwclock --systohc\n')
    setup.write('timedatectl set-ntp true\n')

    setup.write('clear\n')
    setup.write('echo ">> Configuring localization"\n')
    setup.write('read -t 5 -n 1 -s -r -p "Press wait to continue...\n"\n')
    setup.write('echo "' + locale2 + '" >> /etc/locale.gen\n')
    setup.write('locale-gen\n')
    setup.write('echo LANG=' + locale + ' > /etc/locale.conf\n')

    setup.write('clear\n')
    setup.write('echo ">> Configuring keyboard mapping"\n')
    setup.write('read -t 5 -n 1 -s -r -p "Press wait to continue...\n"\n')
    setup.write('localectl --no-convert set-x11-keymap ' + keymap + '\n')
    setup.write('echo KEYMAP=' + keymap + ' > /etc/vconsole.conf\n')

    setup.write('clear\n')
    setup.write('echo ">> Configuring network"\n')
    setup.write('read -t 5 -n 1 -s -r -p "Press wait to continue...\n"\n')
    if nm == "nmcli":
        setup.write('pacman -Syy --noconfirm networkmanager nm-connection-editor\n')
        if desktop_env == "kde":
            setup.write('pacman -Syy --noconfirm plasma-nm\n')
        else:
            setup.write('pacman -Syy --noconfirm network-manager-applet\n')
        setup.write('systemctl enable NetworkManager.service\n')
        if dhcp == "yes":
            setup.write('pacman -Syy --noconfirm dhcpcd\n')
            setup.write('systemctl enable dhcpcd.service\n')
        if wifi_support == "yes":
            setup.write('pacman -Syy --noconfirm wpa_supplicant dialog\n')
        if pppoe_support == "yes":
            setup.write('pacman -Syy --noconfirm rp-pppoe\n')
        if mobile_support == "yes":
            setup.write('pacman -Syy --noconfirm modemmanager mobile-broadband-provider-info usb_modeswitch\n')
    if nm == "wifi-menu":
        setup.write("pacman -Syy --noconfirm netctl\n")
        if dhcp == "yes":
            setup.write('pacman -Syy --noconfirm dhcpcd\n')
            setup.write('systemctl enable dhcpcd.service\n')
        if wifi_support == "yes":
            setup.write('pacman -Syy --noconfirm wpa_supplicant dialog\n')
        if pppoe_support == "yes":
            setup.write('pacman -Syy --noconfirm ppp\n')
        if mobile_support == "yes":
            setup.write('pacman -Syy --noconfirm modemmanager mobile-broadband-provider-info usb_modeswitch\n')

    setup.write('clear\n')
    setup.write('echo ">> Configuring desktop environment - if choosed"\n')
    setup.write('read -t 5 -n 1 -s -r -p "Press wait to continue...\n"\n')
    if desktop_env != "not choosed":
        if desktop_env == "gnome":
            setup.write('pacman -Syy --noconfirm gnome\n')
            setup.write('pacman -Syy --noconfirm gnome-extra\n')
            setup.write('pacman -Syy --noconfirm gdm\n')
            setup.write('systemctl enable gdm\n')
            setup.write('pacman -Syy --noconfirm ttf-inconsolata\n')
            setup.write('pacman -Syy --noconfirm ttf-dejavu\n')
            setup.write('pacman -Syy --noconfirm ttf-font-awesome\n')
            setup.write('pacman -Syy --noconfirm ttf-joypixels\n')
            setup.write('pacman -Syy --noconfirm xdg-user-dirs\n')
            setup.write('pacman -Syy --noconfirm pulseaudio pulseaudio-alsa pavucontrol mpg123 libcdio\n')
        if desktop_env == "kde":
            setup.write('pacman -Syy --noconfirm plasma\n')
            setup.write('pacman -Syy --noconfirm kde-applications\n')
            setup.write('pacman -Syy --noconfirm sddm\n')
            setup.write('systemctl enable sddm\n')
            setup.write('pacman -Syy --noconfirm ttf-inconsolata\n')
            setup.write('pacman -Syy --noconfirm ttf-dejavu\n')
            setup.write('pacman -Syy --noconfirm ttf-font-awesome\n')
            setup.write('pacman -Syy --noconfirm ttf-joypixels\n')
            setup.write('pacman -Syy --noconfirm xdg-user-dirs\n')
            setup.write('pacman -Syy --noconfirm pulseaudio pulseaudio-alsa pavucontrol mpg123 libcdio\n')
        if desktop_env == "mate":
            setup.write('pacman -Syy --noconfirm mate\n')
            setup.write('pacman -Syy --noconfirm mate-extra\n')
            setup.write('pacman -Syy --noconfirm lightdm\n')
            setup.write('pacman -Syy --noconfirm lightdm-gtk-greeter lightdm-gtk-greeter-settings\n')
            setup.write('systemctl enable lightdm.service\n')
            setup.write('pacman -Syy --noconfirm ttf-inconsolata\n')
            setup.write('pacman -Syy --noconfirm ttf-dejavu\n')
            setup.write('pacman -Syy --noconfirm ttf-font-awesome\n')
            setup.write('pacman -Syy --noconfirm ttf-joypixels\n')
            setup.write('pacman -Syy --noconfirm xdg-user-dirs\n')
            setup.write('pacman -Syy --noconfirm pulseaudio pulseaudio-alsa pavucontrol mpg123 libcdio\n')
        if desktop_env == "xfce4":
            setup.write('pacman -Syy --noconfirm xfce4\n')
            setup.write('pacman -Syy --noconfirm xfce4-goodies\n')
            setup.write('pacman -Syy --noconfirm lightdm\n')
            setup.write('pacman -Syy --noconfirm lightdm-gtk-greeter lightdm-gtk-greeter-settings\n')
            setup.write('systemctl enable lightdm.service\n')
            setup.write('pacman -Syy --noconfirm ttf-inconsolata\n')
            setup.write('pacman -Syy --noconfirm ttf-dejavu\n')
            setup.write('pacman -Syy --noconfirm ttf-font-awesome\n')
            setup.write('pacman -Syy --noconfirm ttf-joypixels\n')
            setup.write('pacman -Syy --noconfirm xdg-user-dirs\n')
            setup.write('pacman -Syy --noconfirm pulseaudio pulseaudio-alsa pavucontrol mpg123 libcdio\n')
        if desktop_env == "cinnamon":
            setup.write('pacman -Syy --noconfirm cinnamon\n')
            setup.write('pacman -Syy --noconfirm lightdm\n')
            setup.write('pacman -Syy --noconfirm lightdm-gtk-greeter lightdm-gtk-greeter-settings\n')
            setup.write('systemctl enable lightdm.service\n')
            setup.write('pacman -Syy --noconfirm ttf-inconsolata\n')
            setup.write('pacman -Syy --noconfirm ttf-dejavu\n')
            setup.write('pacman -Syy --noconfirm ttf-font-awesome\n')
            setup.write('pacman -Syy --noconfirm ttf-joypixels\n')
            setup.write('pacman -Syy --noconfirm xdg-user-dirs\n')
            setup.write('pacman -Syy --noconfirm pulseaudio pulseaudio-alsa pavucontrol mpg123 libcdio\n')

    setup.write('clear\n')
    setup.write('echo ">> Configuring video driver - if choosed"\n')
    setup.write('read -t 5 -n 1 -s -r -p "Press wait to continue...\n"\n')
    if video_driver != "not choosed":
        setup.write('pacman -Syy --noconfirm xf86-video-vesa\n')
        setup.write('pacman -Syy --noconfirm mesa\n')
        if video_driver == "nvidia":
            setup.write('pacman -Syy --noconfirm nvidia-dkms nvidia-utils nvidia-settings\n')
        if video_driver == "amd":
            setup.write('pacman -Syy --noconfirm xf86-video-amdgpu\n')
        if video_driver == "intel":
            setup.write('pacman -Syy --noconfirm xf86-video-intel\n')
        if video_driver == "virtualbox":
            setup.write('pacman -Syy --noconfirm virtualbox-guest-utils xf86-video-vmware\n')
            setup.write('systemctl enable vboxservice.service\n')
        setup.write('pacman -Syy --noconfirm xorg-server xorg-xinit xorg-xrandr arandr xterm\n')

    setup.write('clear\n')
    setup.write('echo "> Installing NTFS file system support"\n')
    setup.write('read -t 5 -n 1 -s -r -p "Press wait to continue...\n"\n')
    setup.write('pacman -Syy --noconfirm ntfs-3g\n')
    setup.write('exit\n')
    setup.close()

    if multilib == "yes":
        arch_runcmd("echo \"\" >> /mnt/etc/pacman.conf")
        arch_runcmd("echo \"[multilib]\" >> /mnt/etc/pacman.conf")
        arch_runcmd("echo \"Include = /etc/pacman.d/mirrorlist\" >> /mnt/etc/pacman.conf")

    print(">> Prepare to chroot")
    arch_runcmd("cp setup.sh /mnt/setup.sh")
    arch_runcmd("chmod +x /mnt/setup.sh")
    arch_runcmd("cp /etc/pacman.d/mirrorlist /mnt/etc/pacman.d/mirrorlist")

    print(">> Start configuration")
    arch_runcmd("arch-chroot /mnt bash -c \"./setup.sh\"")

    print("Configuration has been completed!")
    arch_runcmd("rm /mnt/setup.sh")

    t.sleep(5)


def createConfigDir():
    # create config directory
    if o.path.exists("./config") == False:
        o.mkdir("./config")


def readConfig():
    global desktop_env
    global desktop_mngr
    global keymap
    global mobile_support
    global nm
    global timezone
    global video_driver
    global dhcp
    global hostname
    global multilib
    global locale
    global locale2
    global pppoe_support
    global wifi_support
    global users_list
    # load config files to vars
    if o.path.exists("./config/de.conf"):
        config = open("./config/de.conf")
        content = config.read().split("\n")
        desktop_env = content[0]
        config.close()
    if o.path.exists("./config/dm.conf"):
        config = open("./config/dm.conf")
        content = config.read().split("\n")
        desktop_mngr = content[0]
        config.close()
    if o.path.exists("./config/keymap.conf"):
        config = open("./config/keymap.conf")
        content = config.read().split("\n")
        keymap = content[0]
        config.close()
    if o.path.exists("./config/mobile.conf"):
        config = open("./config/mobile.conf")
        content = config.read().split("\n")
        mobile_support = content[0]
        config.close()
    if o.path.exists("./config/network.conf"):
        config = open("./config/network.conf")
        content = config.read().split("\n")
        nm = content[0]
        config.close()
    if o.path.exists("./config/timezone.conf"):
        config = open("./config/timezone.conf")
        content = config.read().split("\n")
        timezone = content[0]
        config.close()
    if o.path.exists("./config/video.conf"):
        config = open("./config/video.conf")
        content = config.read().split("\n")
        video_driver = content[0]
        config.close()
    if o.path.exists("./config/dhcp.conf"):
        config = open("./config/dhcp.conf")
        content = config.read().split("\n")
        dhcp = content[0]
        config.close()
    if o.path.exists("./config/hostname.conf"):
        config = open("./config/hostname.conf")
        content = config.read().split("\n")
        hostname = content[0]
        config.close()
    if o.path.exists("./config/locale.conf"):
        config = open("./config/locale.conf")
        content = config.read().split("\n")
        locale = content[0]
        locale2 = content[1]
        config.close()
    if o.path.exists("./config/multilib.conf"):
        config = open("./config/multilib.conf")
        content = config.read().split("\n")
        multilib = content[0]
        config.close()
    if o.path.exists("./config/pppoe.conf"):
        config = open("./config/pppoe.conf")
        content = config.read().split("\n")
        pppoe_support = content[0]
        config.close()
    if o.path.exists("./config/wifi.conf"):
        config = open("./config/wifi.conf")
        content = config.read().split("\n")
        wifi_support = content[0]
        config.close()
    if o.path.exists("./config/users.conf"):
        config = open("./config/users.conf")
        content = config.read().split("\n")
        for user in content:
            if user != "" and user != "root":
                users_list.append(user)
        config.close()


def arch_install():  # PyArchLinux Installer main menu
    # check efi mode before start!
    print("Checking EFI mode...\n")
    if int(s.check_output("ls /sys/firmware/efi/efivars | wc -l", shell=True)) > 1:
        print("EFI mode: YES\n")
        efi_mode = 1
    else:
        print("EFI mode: NO\n")
        efi_mode = 0
    menu = 1
    while menu == 1:
        clear()
        arch_logo()
        print("               Install Arch Linux as simple as \"1-2-3\"!               ")
        separator()
        print("                          M A I N   M E N U                             ")
        separator()
        print(" 1. Check Internet connection                                           ")
        print(" 2. Disk Management                                                     ")
        print(" 3. Install Arch Linux                                                  ")
        print(" q. Exit                                                                ")
        print("\nYour choice?                                                          ")
        choice = input()
        if choice != "q":
            if choice == "1":
                arch_iptest()
            if choice == "2":
                arch_disk_management(efi_mode)
            if choice == "3":
                arch_setup_menu(efi_mode)
        else:
            clear()
            arch_logo()
            print("Thank You for using PyArchLinux script!\nGoodbye!\n\n\n")
            menu = 0


createConfigDir()
readConfig()
arch_install()
