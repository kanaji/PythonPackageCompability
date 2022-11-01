import subprocess
import sys


class PackageCompatiblity:
    def __init__(self, requirements_filename, compatible_packages_file):
        self.requirements_file = requirements_filename
        self.compatible_packages_file = compatible_packages_file
        self.required_packages = None
        self.compatible_packages = []
        self.incompatible_packages = []

    def read_requirements_file_to_list(self):
        with open(self.requirements_file, "r") as file:
            required_packages = [line.rstrip() for line in file]
        self.required_packages = required_packages

    def install_package(self, package):
        install_output = subprocess.run([sys.executable, "-m", "pip", "install", package], capture_output=True)
        print(install_output.stdout.decode("utf-8"))
        compatible = "Successfully" in install_output.stdout.decode("utf-8")
        if compatible is False:
            return install_output.stdout.decode("utf-8")
        else:
            return True

    def uninstall_package(self, package):
        subprocess.run([sys.executable, "-m", "pip", "uninstall", package, "--quiet", "--yes"])

    def read_compatible_packages(self):
        with open(self.compatible_packages_file, "r") as file:
            compatible_packages = [line.rstrip() for line in file]
        self.compatible_packages = compatible_packages

    def save_compatible_packages_to_file(self):
        f = open(self.compatible_packages_file, "w")
        for package in self.compatible_packages:
            f.write(f"{package}\n")
        f.close()

    def checkPackages(self):
        self.read_compatible_packages()
        self.read_requirements_file_to_list()

        newly_installed_packages_list = []

        for package in self.required_packages:
            if package not in self.compatible_packages:
                status = self.install_package(package)
                if status is True:
                    self.compatible_packages.append(package)
                    newly_installed_packages_list.append(package)
                    print(f"Compatible - {package}")
                else:
                    self.incompatible_packages.append(package)
                    print(f"Incompatible - {package}")
                    print(status)
            else:
                print(f"Compatible - {package}")

        for package in newly_installed_packages_list:
            self.uninstall_package(package)

        self.save_compatible_packages_to_file()


Package_Checker = PackageCompatiblity("requirements_3_11_basic.txt", "compatible_packages.txt")

Package_Checker.install_package("certifi")

# Package_Checker.checkPackages()
