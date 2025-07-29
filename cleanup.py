from utils import globals

def clear_globals():
    globals.current_user_id = None
    globals.encryption_key = None
    print("Globals cleared on app exit.")
