import json
import os

INVENTORY_FILE = "inventory.json"

def get_inventory():
    """Reads the current household inventory from the JSON file."""
    if not os.path.exists(INVENTORY_FILE):
        return "Inventory file not found."
    
    try:
        with open(INVENTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            inventory = data.get("inventory", [])
            
            if not inventory:
                return "The inventory is currently empty."
            
            # Group items by type
            grouped = {}
            for item in inventory:
                itype = item.get("type", "Other")
                if itype not in grouped:
                    grouped[itype] = []
                grouped[itype].append(item)
            
            # Format as a readable string
            lines = ["🏠 **Household Inventory**"]
            for itype, items in grouped.items():
                lines.append(f"\n🔹 **{itype}**")
                for item in items:
                    cat = item.get('category', 'General')
                    lines.append(f"  - {item['item']} ({cat}): {item['quantity']} | Location: {item['storage']}")
            
            return "\n".join(lines)
    except Exception as e:
        return f"Error reading inventory: {str(e)}"

def check_stock(item_name):
    """Checks if a specific item is in stock."""
    if not os.path.exists(INVENTORY_FILE):
        return "Inventory file not found."
        
    try:
        with open(INVENTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            inventory = data.get("inventory", [])
            
            for item in inventory:
                if item_name.lower() in item['item'].lower():
                    return f"We have {item['quantity']} of {item['item']} in the {item['storage']}."
            
            return f"I couldn't find {item_name} in our inventory."
    except Exception as e:
        return f"Error checking stock: {str(e)}"
