#
# PyArchLinux Installer 0.2
# by odziom91
#

# imports
import os as o
import subprocess as s
import time as t

# colors
cyan_black = "\033[1;36;40m " # text cyan, background black
white_black = "\033[1;37;40m " # text white, background black
white_cyan = "\033[1;37;46m " # white text, background cyan

# vars
keymap = "pl"
locale = "pl_PL.UTF-8 UTF-8"
locale2 = "pl_PL.UTF-8"

# clear screen function
def clear():
    o.system("clear")

# PyArchLinux Installer ASCII logo
def arch_logo():
    print(r'%s' %cyan_black)
    print(r'                 `h`                  __________                        ')
    print(r'                 hMd`                 \______   \___.__.                ')
    print(r'                sMMMy                  |     ___<   |  |                ')
    print(r'               +MMMMMs                 |    |    \___  |                ')
    print(r'              /MMMMMMMo                |____|    / ____|                ')
    print(r'             .+mMMMMMMMo                         \/                     ')
    print(r'            /NmyymMMMMMMo                _____                .__       ')
    print(r'           /NMMMMNMMMMMMMo              /  _  \_______   ____ |  |__    ')
    print(r'          +MMMMMMMMMMMMMMMs`           /  /_\  \_  __ \_/ ___\|  |  \   ')
    print(r'         oMMMMMMMMMMMMMMMMMy`         /    |    \  | \/\  \___|   Y  \  ')
    print(r'       `sMMMMMMMmsosdMMMMMMMy`        \____|__  /__|    \___  >___|  /  ')
    print(r'      `yMMMMMMMo`   `oMMMMMMMh`               \/            \/     \/   ')
    print(r'     `hMMMMMMMh       yMMMMMMMd.      .____    .__                      ')
    print(r'    .dMMMMMMMM+       :MMMMMmhys`     |    |   |__| ____  __ _____  ___ ')
    print(r'   -mMMMMMMMMM+       :MMMMMMMNd+`    |    |   |  |/    \|  |  \  \/  / ')
    print(r'  :NMMMMmyo/-``       ``-/oymMMMMN:   |    |___|  |   |  \  |  />    <  ')
    print(r' /NMds:``                   ``:sdMM/  |_______ \__|___|  /____//__/\_ \ ')
    print(r':s:`                             `:s:         \/       \/            \/ ')
    print(r'------------------------------------------------------------------------')
    print(r'                                                 version 0.2            ')
    print(r'------------------------------------------------------------------------')
    print(r'%s' %white_black)

# Running commands
def arch_runcmd(cmd):
    s.call(cmd, shell=True)

# Disk management menu
def arch_disk_management(efi):
    if efi == 1:
        uefi = "YES"
    else:
        uefi = "NO "
    retry = 1
    while retry == 1:
        clear()
        arch_logo()
        print("------------------------------------------------------------------------")
        print("  Disk Management - menu - UEFI mode: " + uefi)
        print("------------------------------------------------------------------------")
        print("")
        print("Note:")
        print("Boot partitions should be prepared on disk with CORRECT disk table!")
        print("For UEFI mode - GPT table")
        print("For BIOS/Legacy mode - MSDOS table")
        print("")
        print(" Choose action:")
        print(" 1. Check disk table")
        print("------------------------------------------------------------------------")
        print(" Use below options with CAUTION! - may destroy your data!")
        print(" 2. Change partition table")
        print(" 3. Create partition")
        print(" 4. Format partition")
        print("------------------------------------------------------------------------")
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

# Arch Linux installation menu
def arch_installation(efi):
    if efi == 1:
        uefi = "YES"
    else:
        uefi = "NO "
    retry = 1
    while retry == 1:
        clear()
        arch_logo()
        print("------------------------------------------------------------------------")
        print("  Install Arch Linux - menu - UEFI mode: " + uefi)
        print("------------------------------------------------------------------------")
        print(" Choose action:")
        print(" 1. Install Arch Linux Base")
        print(" 2. System configuration")
        print(" 3. Add user")
        print(" 4. Install video drivers")
        print(" 5. Install desktop environment")
        print(" 6. Install other packages")
        print(" 0. Exit")
        print(" Your choice?")
        choice = input()
        if choice != "0":
            if choice == "1":
                arch_base(efi)
            if choice == "2":
                arch_configuration()
            if choice == "3":
                arch_users()
            if choice == "4":
                arch_video_driver()
            if choice == "5":
                arch_de()
            if choice == "6":
                arch_pkg()
            retry = 1
        else:
            retry = 0

# Check MBR (MSDOS) and GPT tables
def arch_check_tables(efi):
    if efi == 1:
        uefi = "YES"
    else:
        uefi = "NO "
    retry = 1
    while retry == 1:
        clear()
        arch_logo()
        print("------------------------------------------------------------------------")
        print("  Disk Management - check tables - UEFI mode: " + uefi)
        print("------------------------------------------------------------------------")
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
        retry = 0

# Change disk table - MBR or GPT
def arch_change_table(efi):
    if efi == 1:
        uefi = "YES"
    else:
        uefi = "NO "
    retry = 1
    while retry == 1:
        clear()
        arch_logo()
        print("------------------------------------------------------------------------")
        print("  Disk Management - change partition table - UEFI mode: " + uefi)
        print("------------------------------------------------------------------------")
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

# Disk management - Create partition
def arch_partitioning(efi):
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
        print("------------------------------------------------------------------------")
        print("  Disk Management - create partition - UEFI mode: " + uefi)
        print("------------------------------------------------------------------------")
        print(" Select disk for preparing partitions")
        #arch_runcmd(r'lsblk')
        list_disk = s.check_output("lsblk", shell=True).decode("utf-8").splitlines()
        for line in list_disk:
            if "disk" in line:
                l = line.split()
                disk_table.append(l[0])
                disk_size.append(l[3])
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
                    print("------------------------------------------------------------------------")
                    print("  Disk Management - UEFI mode: " + uefi)
                    print("------------------------------------------------------------------------")
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

# Disk management - Format partition
def arch_formatting(efi):
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
        print("------------------------------------------------------------------------")
        print("  Partition Management - format partition - UEFI mode: " + uefi)
        print("------------------------------------------------------------------------")
        print(" Select partition for formatting")
        list_disk = s.check_output("lsblk -o NAME,SIZE,FSTYPE,TYPE", shell=True).decode("utf-8").splitlines()
        for line in list_disk:
            if "part" in line:
                l = line.split()
                part_table.append(l[0])
                part_size.append(l[1])
                part_type.append(l[2])
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
                print("q. Quit")
                print("")
                print("Your choice?")
                get_fs = input()
                if get_fs != "q":
                    print("Partition: /dev/" + part_table[int(get) - 1].lstrip("└─"))
                    if get_fs == "1":
                        print("File system: ext4")
                    if get_fs == "2":
                        print("File system: fat32")
                    if get_fs == "3":
                        print("File system: swap")
                    print("Are you sure? [y/n]")
                    choice = input()
                    if choice == "y":
                        if get_fs == "1":
                            arch_runcmd("mkfs.ext4 /dev/" + part_table[int(get) - 1].lstrip("└─"))
                        if get_fs == "2":
                            arch_runcmd("mkfs.fat -F32 /dev/" + part_table[int(get) - 1].lstrip("└─"))
                        if get_fs == "3":
                            arch_runcmd("mkswap /dev/" + part_table[int(get) - 1].lstrip("└─"))
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

# Disk management - Mount partition
def arch_mounting(efi):
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
        print("------------------------------------------------------------------------")
        print("  Mount file systems - mount partition - UEFI mode: " + uefi)
        print("------------------------------------------------------------------------")
        print("Select partition for mount")
        list_disk = s.check_output("lsblk -o NAME,SIZE,FSTYPE,TYPE,MOUNTPOINT", shell=True).decode("utf-8").splitlines()
        for line in list_disk:
            if "part" in line:
                l = line.split()
                part_table.append(l[0])
                part_size.append(l[1])
                part_type.append(l[2])
                try:
                    part_mount.append(l[4])
                except Exception:
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
                        arch_runcmd("mount /dev/" + part_table[int(get) - 1].lstrip("└─") + " /mnt")
                    if mnt == "2":
                        arch_runcmd("mkdir -p /mnt/boot")
                        arch_runcmd("umount /mnt/boot")
                        arch_runcmd("mount /dev/" + part_table[int(get) - 1].lstrip("└─") + " /mnt/boot")
                    if mnt == "3":
                        arch_runcmd("mkdir -p /mnt/boot/efi")
                        arch_runcmd("umount /mnt/boot/efi")
                        arch_runcmd("mount /dev/" + part_table[int(get) - 1].lstrip("└─") + " /mnt/boot/efi")
                    if mnt == "4":
                        arch_runcmd("mkdir -p /mnt/home")
                        arch_runcmd("umount /mnt/home")
                        arch_runcmd("mount /dev/" + part_table[int(get) - 1].lstrip("└─") + " /mnt/home")
                    if mnt == "5":
                        arch_runcmd("swapon /dev/" + part_table[int(get) - 1].lstrip("└─"))
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

# Install Arch Linux base to /mnt
def arch_base(efi):
    if efi == 1:
        uefi = "YES"
    else:
        uefi = "NO "
    retry = 1
    while retry == 1:
        clear()
        arch_logo()
        print("------------------------------------------------------------------------")
        print("  Install Arch Linux - base installation - UEFI mode: " + uefi)
        print("------------------------------------------------------------------------")
        print("Please check mount points before continue:")
        arch_runcmd(r'lsblk')
        print("Continue? [y/n]")
        install = input()
        if install == "y":
            print(">> Refresh repositiories")
            arch_runcmd("pacman -Syy")
            print(">> Installing base")
            arch_runcmd("pacstrap /mnt base base-devel linux linux-firmware")
            arch_runcmd("echo \"\" >> /mnt/etc/pacman.conf")
            arch_runcmd("echo \"[multilib]\" >> /mnt/etc/pacman.conf")
            arch_runcmd("echo \"Include = /etc/pacman.d/mirrorlist\" >> /mnt/etc/pacman.conf")
            print(">> Arch Linux base has been installed.")
            t.sleep(5)
            retry = 0
        else:
            retry = 0

# Install video drivers via chroot and generated bash script
def arch_video_driver():
    retry = 1
    while retry == 1:
        clear()
        arch_logo()
        print("------------------------------------------------------------------------")
        print("  Install Arch Linux - video drivers ")
        print("------------------------------------------------------------------------")
        print("Choose your video card vendor:")
        print("1. NVidia")
        print("2. AMD")
        print("3. Intel")
        print("4. VirtualBox")
        print("0. Cancel")
        print("Your choice?")
        video = input()
        if video != "0":
            arch_runcmd("rm setup_video.sh")
            arch_runcmd("rm /mnt/setup_video.sh")
            setup = open("setup_video.sh", "a")
            setup.write("#!/bin/bash\n")
            setup.write("pacman -Syy --noconfirm xf86-video-vesa\n")
            setup.write("pacman -Syy --noconfirm mesa\n")
            if video == "1":
                setup.write("pacman -Syy --noconfirm nvidia nvidia-settings\n")
            if video == "2":
                setup.write("pacman -Syy --noconfirm xf86-video-amdgpu\n")
            if video == "3":
                setup.write("pacman -Syy --noconfirm xf86-video-intel\n")
            if video == "4":
                setup.write("pacman -Syy --noconfirm virtualbox-guest-utils xf86-video-vmware\n")
                setup.write("systemctl enable vboxservice.service\n")
            setup.write("pacman -Syy --noconfirm xorg-server xorg-xinit xorg-xrandr arandr xterm\n")
            setup.write("exit\n")
            setup.close()

            print(">> Prepare to chroot")
            arch_runcmd("cp setup_video.sh /mnt/setup_video.sh")
            arch_runcmd("chmod +x /mnt/setup_video.sh")
            arch_runcmd("arch-chroot /mnt bash -c \"./setup_video.sh\"")
            retry = 0
        else:
            retry = 0

# Install desktop environment via chroot and generated bash script
def arch_de():
    retry = 1
    while retry == 1:
        clear()
        arch_logo()
        print("------------------------------------------------------------------------")
        print("  Install Arch Linux - Desktop Environment ")
        print("------------------------------------------------------------------------")
        print("Choose your video card vendor:")
        print("1. Gnome")
        print("2. KDE Plasma")
        print("3. Mate")
        print("4. Xfce")
        print("5. Cinnamon")
        print("6. Budgie")
        print("7. Deepin")
        print("8. Enlightenment")
        print("9. LXDE")
        print("10. LQxt")
        print("0. Cancel")
        print("Your choice?")
        de = input()
        if de != "0":
            arch_runcmd("rm setup_de.sh")
            arch_runcmd("rm /mnt/setup_de.sh")
            setup = open("setup_de.sh", "a")
            setup.write("#!/bin/bash\n")
            if de == "1":
                setup.write("pacman -Syy --noconfirm gnome\n")
                setup.write("pacman -Syy --noconfirm gnome-extra\n")
            if de == "2":
                setup.write("pacman -Syy --noconfirm plasma\n")
                setup.write("pacman -Syy --noconfirm kde-applications\n")
            if de == "3":
                setup.write("pacman -Syy --noconfirm mate\n")
                setup.write("pacman -Syy --noconfirm mate-extra\n")
            if de == "4":
                setup.write("pacman -Syy --noconfirm xfce4\n")
                setup.write("pacman -Syy --noconfirm xfce4-goodies\n")
            if de == "5":
                setup.write("pacman -Syy --noconfirm cinnamon\n")
            if de == "6":
                setup.write("pacman -Syy --noconfirm budgie-desktop\n")
            if de == "7":
                setup.write("pacman -Syy --noconfirm deepin\n")
                setup.write("pacman -Syy --noconfirm deepin-extra\n")
            if de == "8":
                setup.write("pacman -Syy --noconfirm enlightenment\n")
            if de == "9":
                setup.write("pacman -Syy --noconfirm lxde\n")
            if de == "10":
                setup.write("pacman -Syy --noconfirm lxqt\n")
                setup.write("pacman -Syy --noconfirm breeze-icons\n")
            setup.write("pacman -Syy --noconfirm lightdm\n")
            setup.write("pacman -Syy --noconfirm lightdm-gtk-greeter lightdm-gtk-greeter-settings\n")
            setup.write("pacman -Syy --noconfirm ttf-inconsolata\n")
            setup.write("pacman -Syy --noconfirm ttf-dejavu\n")
            setup.write("pacman -Syy --noconfirm ttf-font-awesome\n")
            setup.write("pacman -Syy --noconfirm ttf-joypixels\n")
            setup.write("pacman -Syy --noconfirm xdg-user-dirs\n")
            setup.write("systemctl enable lightdm.service\n")
            setup.write("pacman -Syy --noconfirm pulseaudio pulseaudio-alsa pavucontrol mpg123 libcdio\n")
            setup.write("exit\n")
            setup.close()

            print(">> Prepare to chroot")
            arch_runcmd("cp setup_de.sh /mnt/setup_de.sh")
            arch_runcmd("chmod +x /mnt/setup_de.sh")
            arch_runcmd("arch-chroot /mnt bash -c \"./setup_de.sh\"")
            arch_runcmd("rm /mnt/setup_de.sh")
            retry = 0
        else:
            retry = 0

# Configure system via chroot and generated bash script
def arch_configuration():
    retry = 1
    while retry == 1:
        clear()
        arch_logo()
        print("------------------------------------------------------------------------")
        print("  Install Arch Linux - configuration ")
        print("------------------------------------------------------------------------")
        print(">> Hostname")
        print("Please provide hostname:")
        hostname = input()
        if hostname == "":
            print("Hostname is required...")
            t.sleep(5)
            retry = 0
        else:
            print(">> Time zone")
            print("Please provide time zone (empty = Europe/Paris):")
            tz = input()
            if tz != "":
                print("Selected time zone: " + tz)
            else:
                tz = "Europe/Paris"
                print("Selected time zone: " + tz)

            print(">> Generate fstab file")
            arch_runcmd("genfstab -U /mnt >> /mnt/etc/fstab")

            print(">> Clear scripts")
            arch_runcmd("rm setup.sh")
            arch_runcmd("rm /mnt/setup.sh")

            print(">> Prepare scripts")
            setup = open("setup.sh", "a")
            setup.write("#!/bin/bash\n")
            setup.write("echo \">> ROOT password:\"\n")
            setup.write("echo \"Insert root password now!\"\n")
            setup.write("passwd\n")
            setup.write("echo \">> Configuring time zone\"\n")
            setup.write("ln -sf /usr/share/zoneinfo/" + tz + " /etc/localtime\n")
            setup.write("timedatectl set-timezone \'" + tz + "\'\n")
            setup.write("echo \">> Configuring system time\"\n")
            setup.write("hwclock --systohc\n")
            setup.write("timedatectl set-ntp true\n")
            setup.write("echo \">> Configuring localization\"\n")
            setup.write("echo \"" + locale + "\" >> /etc/locale.gen\n")
            setup.write("locale-gen\n")
            setup.write("echo LANG=" + locale2 + " > /etc/locale.conf\n")
            setup.write("echo \">> Configuring keyboard mapping\"\n")
            setup.write("echo KEYMAP=" + keymap + " > /etc/vconsole.conf\n")
            setup.write("localectl --no-convert set-x11-keymap " + keymap + "\n")
            setup.write("pacman -Syy --noconfirm sudo iptables dhcpcd iwd\n")
            setup.write("echo \">> Configuring network\"\n")
            setup.write("echo \"> Hostname\"\n")
            setup.write("echo " + hostname + " > /etc/hostname\n")
            setup.write("echo \"> /etc/hosts file\"\n")
            setup.write("echo 127.0.0.1 " + "localhost" + " > /etc/hosts\n")
            setup.write("echo ::1 " + "localhost" + " >> /etc/hosts\n")
            setup.write("echo 127.0.1.1 " + hostname + ".localdomain " + hostname + " >> /etc/hosts\n")
            setup.write("echo \"> Installing DHCP (dhcpcd) and iNet Wireless Daemon (iwd) services\"\n")
            setup.write("pacman -Syy --noconfirm dhcpcd iwd\n")
            setup.write("echo \"> Enabling DHCP service\"\n")
            setup.write("systemctl enable dhcpcd.service\n")
            setup.write("echo \"> Installing NTFS file system support\"\n")
            setup.write("pacman -Syy --noconfirm ntfs-3g\n")
            setup.write("exit\n")
            setup.close()

            print(">> Prepare to chroot")
            arch_runcmd("cp setup.sh /mnt/setup.sh")
            arch_runcmd("chmod +x /mnt/setup.sh")
            arch_runcmd("cp /etc/pacman.d/mirrorlist /mnt/etc/pacman.d/mirrorlist")

            print(">> Start configuration")
            arch_runcmd("arch-chroot /mnt bash -c \"./setup.sh\"")
            arch_runcmd("rm /mnt/setup.sh")

            print("Configuration has been completed!")

            t.sleep(5)
            retry = 0

# Install GRUB bootloader via chroot and generated bash script
def arch_bootloader(efi):
    retry = 1
    while retry == 1:
        clear()
        arch_logo()
        print("------------------------------------------------------------------------")
        print("  Install GRUB Bootloader ")
        print("------------------------------------------------------------------------")
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

# Install optional packages via chroot and generated bash script
def arch_pkg():
    retry = 1
    while retry == 1:
        clear()
        arch_logo()
        print("------------------------------------------------------------------------")
        print("  Install Arch Linux - install other packages")
        print("------------------------------------------------------------------------")
        print("Choose group of apps:")
        print("1. General")
        print("pkgfile htop python python-pip rsync sudo unrar unzip wget zip\n"
              "ffmpeg libnotify tlp bleachbit gparted xdg-user-dirs")
        print("2. Office")
        print("libreoffice-fresh atril")
        print("3. Sound")
        print("alsa-utils pulseaudio pulseaudio-alsa pavucontrol audacious")
        print("4. Video")
        print("vlc")
        print("5. Graphics")
        print("gimp inkscape")
        print("6. Games")
        print("steam lutris")
        print("7. Internet")
        print("firefox, thunderbird")
        print("8. Fonts")
        print("ttf-inconsolata ttf-dejavu ttf-font-awesome ttf-joypixels")
        print("9. yay")
        print("x. Other - goes to chroot mode")
        print("q. Quit")
        print("Your choice?")
        packages = input()
        if packages != "q" and packages != "x":
            arch_runcmd("rm setup_pkg.sh")
            arch_runcmd("rm /mnt/setup_pkg.sh")
            setup = open("setup_pkg.sh", "a")
            setup.write("#!/bin/bash\n")
            if packages == "1":
                setup.write("pacman -Syy --noconfirm pkgfile htop python python-pip rsync sudo unrar unzip wget zip ffmpeg libnotify tlp bleachbit gparted\n")
            if packages == "2":
                setup.write("pacman -Syy --noconfirm libreoffice-fresh atril\n")
            if packages == "3":
                setup.write("pacman -Syy --noconfirm alsa-utils pulseaudio pulseaudio-alsa pavucontrol audacious audacious-plugins\n")
            if packages == "4":
                setup.write("pacman -Syy --noconfirm vlc\n")
            if packages == "5":
                setup.write("pacman -Syy --noconfirm gimp inkscape\n")
            if packages == "6":
                setup.write("pacman -Syy --noconfirm steam lutris\n")
            if packages == "7":
                setup.write("pacman -Syy --noconfirm firefox thunderbird\n")
            if packages == "8":
                setup.write("pacman -Syy --noconfirm ttf-inconsolata ttf-dejavu ttf-font-awesome ttf-joypixels\n")
            if packages == "9":
                setup.write("pacman -Syy --noconfirm git\n")
                setup.write("cd /root\n")
                setup.write("git clone https://aur.archlinux.org/yay.git\n")
                setup.write("cd yay\n")
                setup.write("makepkg -si\n")
            setup.write("exit\n")
            setup.close()

            print(">> Prepare to chroot")
            arch_runcmd("cp setup_pkg.sh /mnt/setup_pkg.sh")
            arch_runcmd("chmod +x /mnt/setup_pkg.sh")
            arch_runcmd("arch-chroot /mnt bash -c \"./setup_pkg.sh\"")
            arch_runcmd("rm /mnt/setup_pkg.sh")
            retry = 0
        if packages == "x":
            arch_runcmd("arch-chroot /mnt")
            retry == 1
        if packages == "0":
            retry = 0

# Install  via chroot and generated bash script
def arch_users():
    retry = 1
    while retry == 1:
        clear()
        arch_logo()
        print("------------------------------------------------------------------------")
        print("  Install Arch Linux - add user")
        print("------------------------------------------------------------------------")
        print("Enter username:")
        username = input()
        print("Enter group:")
        group = input()
        if username != "":
            if group == "":
                group = "users"
            arch_runcmd("rm setup_user.sh")
            arch_runcmd("rm /mnt/setup_user.sh")
            setup = open("setup_user.sh", "a")
            setup.write("#!/bin/bash\n")
            setup.write("groupadd " + group + "\n")
            setup.write("useradd -m -g " + group + " " + username + "\n")
            setup.write("passwd " + username + "\n")
            setup.write("exit\n")
            setup.close()
            arch_runcmd("cp setup_user.sh /mnt/setup_user.sh")
            arch_runcmd("chmod +x /mnt/setup_user.sh")
            arch_runcmd("arch-chroot /mnt bash -c \"./setup_user.sh\"")
            arch_runcmd("rm /mnt/setup_user.sh")
            t.sleep(3)
            retry = 0
        else:
            print("Username not entered.")
            t.sleep(3)
            retry = 0

# PyArchLinux Installer main menu
def arch_install():
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
        print("------------------------------------------------------------------------")
        print("                          M A I N   M E N U                             ")
        print("------------------------------------------------------------------------")
        print(" 0. Check Internet connection                                           ")
        print(" 1. Disk Management                                                     ")
        print(" 2. Install Arch Linux                                                  ")
        print(" 3. Install bootloader                                                  ")
        print(" q. Exit                                                                ")
        print("\nYour choice?                                                          ")
        choice = input()
        if choice != "q":
            if choice == "0":
                print("Pinging archlinux.org for 10 times...")
                arch_runcmd("ping -c 10 archlinux.org")
                print("Please wait...")
                t.sleep(5)
            if choice == "1":
                arch_disk_management(efi_mode)
            if choice == "2":
                arch_installation(efi_mode)
            if choice == "3":
                arch_bootloader(efi_mode)
        else:
            clear()
            arch_logo()
            print("Goodbye!\n\n\n")
            menu = 0

arch_install()
