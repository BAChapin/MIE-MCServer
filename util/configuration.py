from .mielib import custominput as ci
import yaml, os

class File:
    __util_dir = os.path.dirname(__file__)
    __root_dir = os.path.join(__util_dir, "..")
    __file_dir = os.path.join(__root_dir, "config.yml")
    if os.path.exists(__file_dir):
        __file = open(__file_dir, "r")
        data = yaml.load(__file, yaml.Loader)
    else:
        data = {}

    exists = os.path.isfile(__file_dir)

    @classmethod
    def update(cls, section, update):
        with open(cls.__file_dir, "w") as file:
            cls.data[section] = update
            yaml.dump(cls.data, file, default_flow_style=False)

    @classmethod
    def generate(cls):
        Minecraft.reset()
        Email.reset()
        Maintenance.reset()

        if os.path.exists(cls.__file_dir):
            os.remove(cls.__file_dir)
        
        Minecraft.update()
        Email.update()
        Maintenance.update()

    @classmethod
    def build(cls):
        if os.path.exists(cls.__file_dir):
            user_response = ci.bool_input("This will override your current " \
                "config.yml, are you sure you want to do that?", default=False)
            if user_response:
                os.remove(cls.__file_dir)
            else:
                return False

        print("I will ask a series of questions to build your config.yml\n" \
            "You are free to edit your config.yml file manually after creation.")

        Email.build()
        # Minecraft.build()
        Maintenance.build()

        return True

        # os.remove(cls.__file_dir)
        # file = open(cls.__file_dir, "w")
        # yaml.dump(config, file, default_flow_style=False)

class Minecraft:
    SECTION_NAME = "Minecraft"
    __data = File.data.get("Minecraft", {})
    __version = __data.get("version", {})
    allocated_ram = int(__data.get("allocated_ram", 1024))
    major = __version.get("major", None)
    minor = __version.get("minor", None)
    patch = __version.get("patch", None)
    build = __version.get("build", None)
    install_date = __version.get("install_date", "")
    version_group = __version.get("version_group", None)

    @classmethod
    def version_str(cls):
        if cls.patch is None:
            return "{}.{}:{}".format(cls.major, cls.minor, cls.build)
        else:
            return "{}.{}.{}:{}".format(cls.major, cls.minor, cls.patch, cls.build)

    @classmethod
    def build(cls):
        ram = ci.int_input("How much RAM would you like to dedicate to your " \
            "Minecraft Server? (your input will be Mbs)", default=512)
        # version_str = input("What version would you like to install? [#.##.#] ")
        # version = ci.regex_input("What version would you like to install?", 
        #                       regex="#.##.#/#.##",
        #                       default="1.17.1")
        should_update = ci.bool_input("Would you like to allow major updates? "\
            "(we caution against this due to early release bugs)", default=False)
        

    @classmethod
    def update(cls):
        cls.__version["major"] = cls.major
        cls.__version["minor"] = cls.minor
        cls.__version["patch"] = cls.patch
        cls.__version["build"] = cls.build
        cls.__version["install_date"] = cls.install_date
        cls.__version["version_group"] = cls.version_group
        cls.__data["allocated_ram"] = cls.allocated_ram
        cls.__data["version"] = cls.__version
        File.update(cls.SECTION_NAME, cls.__data)

    @classmethod
    def reset(cls):
        cls.allocated_ram = 1024
        cls.major = None
        cls.minor = None
        cls.patch = None
        cls.build = None
        cls.install_date = ""
        cls.version_group = None


class Email:
    SECTION_NAME = "Email"
    __data = File.data.get("Email", {})
    address = __data.get("address", "<your.email@gmail.com>")
    password = __data.get("password", "<your password>")
    server = __data.get("server", "smtp.gmail.com")
    port = __data.get("port", 587)
    recipients = __data.get("recipients", [])

    @classmethod
    def build(cls):
        email_address = ci.email_input("What is the gmail address you would " \
            "like me to use to send you reports?", provider="gmail")
        password = ci.confirm_input("What is the password to the account you " \
            "just enetered? ")
        recipients = ci.email_input("What email address(es) would you like " \
            "to recieve the logs and reports?", multiples=True)
        cls.address = email_address
        cls.password = password
        print(recipients)
        cls.recipients = recipients
        cls.update()

    @classmethod
    def update(cls):
        cls.__data["address"] = cls.address
        cls.__data["password"] = cls.password
        cls.__data["server"] = cls.server
        cls.__data["port"] = cls.port
        cls.__data["recipients"] = cls.recipients
        File.update(cls.SECTION_NAME, cls.__data)

    @classmethod
    def reset(cls):
        cls.address = "<your.email@gmail.com>"
        cls.password = "<your password>"
        cls.server = "smtp.gmail.com"
        cls.port = 587
        cls.recipients = []


class Maintenance:
    SECTION_NAME = "Maintenance"
    __data = File.data.get("Maintenance", {})
    __backup = __data.get("backup", {})
    __update = __data.get("update", {})
    complete_shutdown = __data.get("complete_shutdown", "")
    schedule = __data.get("schedule", "")
    backup_schedule = __backup.get("schedule", "")
    backup_path = __backup.get("path", "~/MC_Backups")
    backup_number = __backup.get("number", 1)
    update_schedule = __update.get("schedule", "")
    update_allow_major_update = __update.get("allow_major_update", False)

    @classmethod
    def build(cls):
        print("Warning: A system restart is good practice to clear out any " \
            "residual problems that might still be in RAM. Also, in order to " \
            "run the commands file a server restart is required.")
        restart_cron = ci.cron_date_input("restart")

        print("Warning: It is good practice to backup your server so if any" \
            "thing were to happen, you would be able to revert back to your " \
            "previous backup.")
        backup_cron = ci.cron_date_input("backup Minecraft")
        backup_path = input("Where would you like your backups to be stored? ")
        backup_limit = ci.int_input("How many backups would you like to be " \
            "stored before removing old backups?")

        print("Warning: It is wise to check for updates on a regular basis so " \
            "any bugs the developers might find and fix will be applied to " \
            "your server. We can understand your concern for larger updates, " \
            "so we will ask your permission on if you want us to do bigger " \
            "updates automatically. If not, we will email you and alert you " \
            "of any major updates.")
        update_cron = ci.cron_date_input("check for updates")
        major_updates = ci.bool_input("Would you like me to update to " \
            "major releases?", default=False)
            
        print("Warning: I have ben preprogrammed with some useful maintenance " \
            "scripts to help keep your server up and running smoothly. It is " \
            "always good to run these scripts so your players experience as " \
            "little server lag as possible.")
        maintenance_cron = ci.cron_date_input("run maintenance scripts")

        cls.complete_shutdown = restart_cron
        cls.schedule = maintenance_cron
        cls.backup_schedule = backup_cron
        cls.backup_path = backup_path
        cls.backup_number = backup_limit
        cls.update_schedule = update_cron
        cls.update_allow_major_update = major_updates
        cls.update()

    @classmethod
    def update(cls):
        cls.__backup["schedule"] = cls.backup_schedule
        cls.__backup["path"] = cls.backup_path
        cls.__backup["number"] = cls.backup_number
        cls.__update["schedule"] = cls.update_schedule
        cls.__update["allow_major_update"] = cls.update_allow_major_update
        cls.__data["complete_shutdown"] = cls.complete_shutdown
        cls.__data["schedule"] = cls.schedule
        cls.__data["backup"] = cls.__backup
        cls.__data["update"] = cls.__update
        File.update(cls.SECTION_NAME, cls.__data)

    @classmethod
    def reset(cls):
        cls.complete_shutdown = ""
        cls.schedule = ""
        cls.backup_schedule = ""
        cls.backup_path = "~/MC_Backups"
        cls.backup_number = 1
        cls.update_schedule = ""
        cls.update_allow_major_update = False
