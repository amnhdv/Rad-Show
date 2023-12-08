import os
import subprocess
import curses
import curses.textpad
import platform

DNS_PROVIDERS = {
    'Google': ['8.8.8.8', '8.8.4.4'],
    'OpenDNS': ['208.67.222.222', '208.67.220.220'],
    'Cloudflare': ['1.1.1.1', '1.0.0.1'],
    'Quad9': ['9.9.9.9', '149.112.112.112'],
    'Shecan': ['178.22.122.100', '185.51.200.2'],
    'Begzar': ['185.55.225.25', '185.55.226.26'],
    '403': ['10.202.10.202', '10.202.10.102'],
    'Radar': ['10.202.10.10', '10.202.10.11'],
    'Electro': ['78.157.42.100', '78.157.42.101']
}

APP_NAME_ASCII = """
 ___  __  __     __ _  _  __  _   _  
| _ \/  \| _\  /' _| || |/__\| | | | 
| v | /\ | v | `._\| >< | \/ | 'V' | 
|_|_|_||_|__/  |___|_||_|\__/!_/ \_! 
"""

class RadShowApp:
    def __init__(self, screen):
        self.screen = screen
        self.selected_option = 0
        self.options = list(DNS_PROVIDERS.keys())
        self.options.extend(['Network Default', 'Flush DNS Cache', 'Quit'])
        self.rows = len(self.options) // 3 + (1 if len(self.options) % 3 else 0)
        self.cols = min(3, len(self.options))

    def run(self):
        """
        Run the program indefinitely.

        This function displays the menu and processes user input
        in a loop until the program is terminated.
        """
        while True:
            self.display_menu()
            self.process_input()

    def display_menu(self):
        self.screen.clear()
        self.screen.box()
        # Print the logo with a rainbow effect
        ascii_lines = APP_NAME_ASCII.split('\n')
        for i, line in enumerate(ascii_lines):
            # Use a different color pair for each line of the logo
            color_pair = curses.color_pair(i + 2)
            self.screen.attron(color_pair)
            self.screen.addstr(i + 1, (curses.COLS - len(line)) // 2, line)
            self.screen.attroff(color_pair)


        start_y = len(ascii_lines) + 2
        box_width = max(len(option) for option in self.options) + 4
        box_height = 3
        # Adjust the margins to center the menu options
        margin_x = (curses.COLS - box_width * self.cols - 2) // (self.cols + 1)
        margin_y = (curses.LINES - start_y - box_height * self.rows - 2) // (self.rows + 1)

        for i, option in enumerate(self.options):
            row = i // self.cols
            col = i % self.cols
            y = start_y + margin_y * row + box_height * row
            x = margin_x * (col + 1) + box_width * col + 1
            attr = self.get_option_attr(i)
            self.print_option(option, y, x, attr, box_width, box_height)

        self.screen.refresh()


    def get_option_attr(self, index):
        """
        Returns the color attribute for the given option index.

        Args:
            index (int): The index of the option.

        Returns:
            int: The color attribute for the option.
        """
        if index == self.selected_option:
            return curses.color_pair(1)
        return curses.color_pair(0)

    def print_option(self, option, y, x, attr, box_width, box_height):
        """
        Print an option within a box on the screen.
        Args:
            option (str): The text of the option.
            y (int): The y-coordinate of the top-left corner of the box.
            x (int): The x-coordinate of the top-left corner of the box.
            attr (int): The attribute for the text formatting.
            box_width (int): The width of the box.
            box_height (int): The height of the box.
        """
        # Enable text formatting with attr
        self.screen.attron(attr)
        # Use the same box_width and box_height as in draw_box method
        self.screen.addstr(y - 1, x, '+' + '-' * (box_width - 2) + '+')
        self.screen.addstr(y, x, '| ' + option.center(box_width - 4) + ' |')
        self.screen.addstr(y + 1, x, '+' + '-' * (box_width - 2) + '+')
        self.screen.attroff(attr)

    def process_input(self):
        """
        Process user input and perform corresponding actions.
        """
        key = self.screen.getch()

        # Move up if possible
        if key == curses.KEY_UP and self.selected_option >= self.cols:
            self.selected_option -= self.cols

        # Move down if possible
        elif key == curses.KEY_DOWN and self.selected_option < len(self.options) - self.cols:
            self.selected_option += self.cols

        # Move left if possible
        elif key == curses.KEY_LEFT and self.selected_option % self.cols > 0:
            self.selected_option -= 1

        # Move right if possible
        elif key == curses.KEY_RIGHT and self.selected_option % self.cols < self.cols - 1 and self.selected_option < len(self.options) - 1:
            self.selected_option += 1

        # Perform action based on selected option
        elif key in [curses.KEY_ENTER, 13, 10]:
            action = self.options[self.selected_option]

            if action == 'Network Default':
                self.confirm_action('reset to network default', self.reset_dns)

            elif action == 'Flush DNS Cache':
                self.confirm_action('flush DNS cache', self.flush_cache)

            elif action == 'Quit':
                self.confirm_action('quit', self.quit_app)

            elif action in DNS_PROVIDERS.keys():
                self.confirm_action(f"use {action}", self.set_dns)
        
        # Cycle between Quad9 and Quit by typing 'q'
        elif key in [ord('q'), ord('Q')]:
            current_option = self.options[self.selected_option]
            if current_option == 'Quad9':
                self.selected_option = self.options.index('Quit')
            else:
                self.selected_option = self.options.index('Quad9')
        
        # Select option by typing the first letter
        elif key >= ord('A') and key <= ord('z'):
            typed_letter = chr(key).upper()
            matching_options = [index for index, option in enumerate(self.options) if option.startswith(typed_letter)]
            if matching_options:
                self.selected_option = matching_options[0]
        
            # Select option "403" by typing '4'
        elif key == ord('4'):
            matching_options = [index for index, option in enumerate(self.options) if option == '403']
            if matching_options:
                self.selected_option = matching_options[0]
                
        self.display_menu()


    def confirm_action(self, action_name, action_function):
        # Get the screen size
        height, width = self.screen.getmaxyx()

        # Create a new window for the confirmation box
        win = curses.newwin(5, 40, height // 2 - 3, width // 2 - 20)

        # Draw a border around the window
        win.border()

        # Write the title and the text
        win.addstr(0, 2, "Confirm Action", curses.A_BOLD)
        win.addstr(2, 2, f"Do you want to {action_name}? (y/n)")

        # Refresh the window
        win.refresh()

        # Set the window to accept keypad input
        win.keypad(True)

        # Loop until a valid input is received
        while True:
            # Get the user input
            key = win.getch()

            # Perform the action if the answer is yes
            if key in [ord('y'), ord('Y')]:
                action_function()
                break

            # Exit the loop if the answer is no
            elif key in [ord('n'), ord('N')]:
                break

        # Clear the window
        win.clear()
        win.refresh()
        

    def set_dns(self):
        provider = self.options[self.selected_option]
        dns_ips = DNS_PROVIDERS[provider]
        
        if platform.system() == "Darwin":
            command = f"networksetup -setdnsservers Wi-Fi {dns_ips[0]} {dns_ips[1]}"
        elif platform.system() == "Linux":
            device_name = subprocess.check_output(["nmcli", "device", "show"]).decode().split()[0]
            command = f"nmcli device modify {device_name} ipv4.dns '{dns_ips[0]} {dns_ips[1]}'"
        else:
            # Handle unsupported platforms or fallback to a default behavior
            self.display_warning("Unsupported operating system")
            return
        
        subprocess.call(command, shell=True)
        self.display_menu()
        self.display_confirmation(f"DNS set to {provider}\n({dns_ips[0]}, {dns_ips[1]})")

    def reset_dns(self):
        if platform.system() == "Darwin":
            command = "networksetup -setdnsservers Wi-Fi Empty"
        elif platform.system() == "Linux":
            command = "nmcli device modify <device_name> ipv4.ignore-auto-dns yes"
        else:
            self.display_warning("Unsupported operating system")
            return
        
        subprocess.call(command, shell=True)
        self.display_menu()
        self.display_confirmation("DNS reset to network default")

    def flush_cache(self):
        if platform.system() == "Darwin":
            command = "dscacheutil -flushcache"
        elif platform.system() == "Linux":
            command = "/etc/init.d/nscd restart"
        else:
            self.display_warning("Unsupported operating system")
            return
        
        subprocess.call(command, shell=True)
        self.display_menu()
        self.display_confirmation("DNS cache flushed")

    def quit_app(self):
        self.display_menu()
        self.display_confirmation("Quitting App")
        curses.endwin()
        exit()

    def draw_box(self, message):
        lines = message.split('\n')
        max_width = max(len(line) for line in lines)

        box_width = max_width + 4
        box_height = len(lines) + 4
        box_y = (curses.LINES - box_height) // 2
        box_x = (curses.COLS - box_width) // 2

        # Use the same box_width and box_height as in print_option method
        # Add some padding to the message lines
        for i in range(box_height):
            if i == 0 or i == box_height - 1:
                line = '+' + '-' * (box_width - 2) + '+'
            elif i == 1 or i == box_height - 2:
                line = '| ' + ' ' * (box_width - 4) + ' |'
            else:
                line = '| ' + lines[i - 2].center(max_width) + ' |'
            # Center the line horizontally and vertically
            y = box_y + i
            x = (curses.COLS - len(line)) // 2
            # Use the default color pair for the box
            attr = curses.color_pair(1)
            # Print the line with the attribute
            self.screen.attron(attr)
            self.screen.addstr(y, x, line)
            self.screen.attroff(attr)

    def display_confirmation(self, message):
        # Clear the screen before displaying the confirmation
        # Use the default color pair for the screen border
        attr = curses.color_pair(0)
        # Draw a border around the screen with the attribute
        self.screen.attron(attr)
        self.screen.border()
        # Turn off the attribute
        self.screen.attroff(attr)

        # Draw a box with the message inside it
        self.draw_box(message)

        # Refresh the screen to show the changes
        self.screen.refresh()
        
         # Display confirmation for 1.5 second
        curses.napms(1500)

         # Clear the screen after displaying the confirmation
         # Refresh the screen again to show the changes
        self.screen.clear()
        self.screen.refresh()

def main(stdscr):
    curses.curs_set(0)
    curses.use_default_colors()
    curses.init_pair(0, -1, -1)  # Default color
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)  # Selected menu option color
    curses.init_pair(2, curses.COLOR_RED, -1)  # Red on default
    curses.init_pair(3, curses.COLOR_GREEN, -1)  # Green on default
    curses.init_pair(4, curses.COLOR_YELLOW, -1)  # Yellow on default
    curses.init_pair(5, curses.COLOR_BLUE, -1)  # Blue on default
    curses.init_pair(6, curses.COLOR_MAGENTA, -1)  # Magenta on default
    curses.init_pair(7, curses.COLOR_CYAN, -1)  # Cyan on default
    stdscr.keypad(True)  # Enable function key support (like Arrow keys)

    app = RadShowApp(stdscr)
    app.run()

curses.wrapper(main)