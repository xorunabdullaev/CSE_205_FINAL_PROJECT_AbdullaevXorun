import json
import os


class Item:
    def __init__(self, item_id, item_name, category, location_found, status="Unclaimed"):
        self.item_id = item_id
        self.item_name = item_name
        self.category = category
        self.location_found = location_found
        self.status = status

    def to_dict(self):
        return {
            "item_id": self.item_id,
            "item_name": self.item_name,
            "category": self.category,
            "location_found": self.location_found,
            "status": self.status
        }

    def from_dict(data):
        return Item(
            data["item_id"],
            data["item_name"],
            data["category"],
            data["location_found"],
            data["status"]
        )


class LostAndFoundSystem:
    def __init__(self, filename="lost_and_found.json"):
        self.filename = filename
        self.items = []
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.filename):
            self.items = []
            return

        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
                self.items = [Item.from_dict(item) for item in data]
        except (json.JSONDecodeError, FileNotFoundError):
            self.items = []

    def save_data(self):
        with open(self.filename, "w") as file:
            json.dump([item.to_dict() for item in self.items], file, indent=4)


    def generate_item_id(self):
        if not self.items:
            return 1
        return max(item.item_id for item in self.items) + 1

    def add_item(self):
        print("\n=== Add Lost Item ===")

        item_name = input("Enter item name: ").strip()
        category = input("Enter category: ").strip()
        location_found = input("Enter location found: ").strip()

        if not item_name or not category or not location_found:
            print("All fields are required!")
            return

        item_id = self.generate_item_id()

        new_item = Item(
            item_id,
            item_name,
            category,
            location_found
        )

        self.items.append(new_item)
        self.save_data()

        print(f"Item added successfully with ID: {item_id}")

    def view_all_items(self):
        print("\n=== All Lost & Found Items ===")

        if not self.items:
            print("No items found.")
            return


        sorted_items = sorted(self.items, key=lambda x: x.category.lower())

        for item in sorted_items:
            print("-" * 40)
            print(f"Item ID        : {item.item_id}")
            print(f"Item Name      : {item.item_name}")
            print(f"Category       : {item.category}")
            print(f"Location Found : {item.location_found}")
            print(f"Status         : {item.status}")

    def search_item(self):
        print("\n=== Search Item ===")
        print("1. Search by Name")
        print("2. Search by Category")
        print("3. Search by Location")

        choice = input("Choose option: ").strip()

        if choice == "1":
            keyword = input("Enter item name: ").strip().lower()
            results = [
                item for item in self.items
                if keyword in item.item_name.lower()
            ]

        elif choice == "2":
            keyword = input("Enter category: ").strip().lower()
            results = [
                item for item in self.items
                if keyword in item.category.lower()
            ]

        elif choice == "3":
            keyword = input("Enter location: ").strip().lower()
            results = [
                item for item in self.items
                if keyword in item.location_found.lower()
            ]

        else:
            print("Invalid choice!")
            return

        if not results:
            print("No matching items found.")
            return

        print("\n=== Search Results ===")
        for item in results:
            print("-" * 40)
            print(f"Item ID        : {item.item_id}")
            print(f"Item Name      : {item.item_name}")
            print(f"Category       : {item.category}")
            print(f"Location Found : {item.location_found}")
            print(f"Status         : {item.status}")

    def mark_as_claimed(self):
        print("\n=== Mark Item as Claimed ===")

        try:
            item_id = int(input("Enter Item ID: "))
        except ValueError:
            print("Invalid ID! Please enter a number.")
            return

        for item in self.items:
            if item.item_id == item_id:
                if item.status == "Claimed":
                    print("Item is already claimed.")
                else:
                    item.status = "Claimed"
                    self.save_data()
                    print("Item marked as claimed successfully.")
                return

        print("Item not found.")

    def delete_item(self):
        print("\n=== Delete Item ===")

        try:
            item_id = int(input("Enter Item ID to delete: "))
        except ValueError:
            print("Invalid ID! Please enter a number.")
            return

        for item in self.items:
            if item.item_id == item_id:
                self.items.remove(item)
                self.save_data()
                print("Item deleted successfully.")
                return

        print("Item not found.")

  
    def count_claimed_items(self):
        claimed = sum(1 for item in self.items if item.status == "Claimed")
        print(f"Total Claimed Items: {claimed}")

    def count_unclaimed_items(self):
        unclaimed = sum(1 for item in self.items if item.status == "Unclaimed")
        print(f"Total Unclaimed Items: {unclaimed}")


    def menu(self):
        while True:
            print("\n========== Lost & Found Management System ==========")
            print("1. Add Lost Item")
            print("2. View All Items")
            print("3. Search Item")
            print("4. Mark Item as Claimed")
            print("5. Delete Item")
            print("6. Count Claimed Items")
            print("7. Count Unclaimed Items")
            print("8. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.add_item()

            elif choice == "2":
                self.view_all_items()

            elif choice == "3":
                self.search_item()

            elif choice == "4":
                self.mark_as_claimed()

            elif choice == "5":
                self.delete_item()

            elif choice == "6":
                self.count_claimed_items()

            elif choice == "7":
                self.count_unclaimed_items()

            elif choice == "8":
                print("Exiting program...")
                break

            else:
                print("Invalid choice! Please try again.")



if __name__ == "__main__":
    system = LostAndFoundSystem()
    system.menu()
 

