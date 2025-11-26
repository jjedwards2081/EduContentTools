#!/usr/bin/env python3
"""
Minecraft Education Content Tools
A CLI application for managing Minecraft Education game information with Azure OpenAI integration.
"""

import os
import sys
from game_manager import GameManager
from settings import Settings


def main():
    """Main entry point for CLI application."""
    app = EduContentTools()
    app.run()


class EduContentTools:
    def __init__(self):
        self.settings = Settings()
        self.game_manager = GameManager(self.settings)
        self.current_game = None
        
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def display_main_menu(self):
        """Display the main menu."""
        self.clear_screen()
        print("=" * 70)
        print("    MINECRAFT EDUCATION CONTENT TOOLS")
        print("=" * 70)
        
        if self.current_game:
            print(f"\n Current Game: {self.current_game}")
            
            # Show quick status
            info = self.game_manager.load_game_info(self.current_game)
            status_items = []
            if info:
                if info.get("world_files"): status_items.append("World [OK]")
                if info.get("context"): status_items.append("Context [OK]")
                if info.get("gameplay"): status_items.append("Gameplay [OK]")
                if info.get("objectives"): status_items.append("Objectives [OK]")
                
                metadata = self.game_manager._load_metadata(self.current_game)
                if metadata and metadata.get("lang_file"):
                    status_items.append("Lang [OK]")
                if info.get("lang_analysis"):
                    status_items.append("Analysis [OK]")
                if metadata and metadata.get("documents"):
                    doc_count = len(metadata["documents"])
                    status_items.append(f"Docs({doc_count}) [OK]")
            
            if status_items:
                print(f"   Status: {' | '.join(status_items)}")
        else:
            print(f"\n No game loaded - Start by creating or loading a game")
        
        print("\n" + "-" * 70)
        print("GAME MANAGEMENT:")
        print("  1. Create New Game")
        print("  2. Load Existing Game")
        print("  3. Upload World File to Current Game")
        
        if self.current_game:
            print("\nCONTENT CREATION:")
            print("  4. Add/Edit Game Context")
            print("  5. Add/Edit Gameplay Description")
            print("  6. Add/Edit Learning Objectives")
            print("  7. Extract & Analyze Language Files")
            print("  d. Upload & Analyze Documents (PDF/Word/PPT)")
            print("  r. Remove Documents")
            
            print("\nCREATION:")
            print("  a. Create Student Guide")
            print("  b. Create Student Workbook")
            print("  c. Create Student Quiz")
            print("  p. Create Parent Guide")
            print("  t. Create Teacher Guide")
            print("  sl. Create School Leadership Information Sheet")
            print("  cs. Create Curriculum Standards Mapping")
            print("  tc. Create Text Complexity Analysis")
            
            print("\nEXPORT:")
            print("  e. Export All Creations to Folder")
        
        print("\nOTHER:")
        print("  s. Settings (Azure OpenAI API)")
        if self.current_game:
            print("  l. List All Games")
        print("  x. Delete Game Folder")
        print("  0. Exit")
        print("-" * 70)
    
    def wait_for_key(self):
        """Wait for user to press Enter."""
        input("\nPress Enter to continue...")
    
    def delete_game(self):
        """Delete a game folder."""
        self.clear_screen()
        print("=" * 70)
        print("    DELETE GAME FOLDER")
        print("=" * 70)
        
        # List all games
        games = self.game_manager.list_games()
        
        if not games:
            print("\n[ERROR] No game folders found!")
            self.wait_for_key()
            return
        
        print("\nAvailable games:")
        print("-" * 70)
        for i, game in enumerate(games, 1):
            status = "(Current)" if game == self.current_game else ""
            print(f"{i}. {game} {status}")
        print("-" * 70)
        
        try:
            choice = input("\nEnter game number to delete (0 to cancel): ").strip()
            
            if choice == "0":
                return
            
            game_index = int(choice) - 1
            if 0 <= game_index < len(games):
                game_to_delete = games[game_index]
                
                # Confirm deletion
                print(f"\n[WARNING]  WARNING: This will permanently delete '{game_to_delete}' and all its contents!")
                print("   This includes:")
                print("   - World files")
                print("   - Documents")
                print("   - Language analysis")
                print("   - All created resources (guides, workbooks, etc.)")
                print("   - Exported files")
                
                confirm = input(f"\nType '{game_to_delete}' to confirm deletion: ").strip()
                
                if confirm == game_to_delete:
                    if self.game_manager.delete_game_folder(game_to_delete):
                        print(f"\n[OK] Successfully deleted '{game_to_delete}'")
                        
                        # If deleted game was current, clear it
                        if self.current_game == game_to_delete:
                            self.current_game = None
                            print("\n[OK] Current game cleared")
                    else:
                        print(f"\n[ERROR] Failed to delete '{game_to_delete}'")
                else:
                    print("\n[ERROR] Deletion cancelled - name didn't match")
            else:
                print("\n[ERROR] Invalid game number!")
        except ValueError:
            print("\n[ERROR] Please enter a valid number!")
        
        self.wait_for_key()
    
    def create_new_game(self):
        """Create a new game folder."""
        self.clear_screen()
        print("=" * 70)
        print("    CREATE NEW GAME")
        print("=" * 70)
        
        game_name = input("\nEnter game name: ").strip()
        if not game_name:
            print("\n[ERROR] Game name cannot be empty!")
            self.wait_for_key()
            return
        
        result = self.game_manager.create_game_folder(game_name)
        if result:
            self.current_game = game_name
            print(f"\n[OK] Game folder '{game_name}' created successfully!")
            
            # Prompt to upload world file
            upload = input("\nWould you like to upload a world file now? (y/n): ").strip().lower()
            if upload == 'y':
                world_files = self.game_manager.list_world_files_in_downloads()
                if world_files:
                    print("\nAvailable world files in Downloads:")
                    for i, file in enumerate(world_files, 1):
                        filename = file.split('/')[-1]
                        print(f"{i}. {filename}")
                    
                    try:
                        selection = int(input("\nSelect file number (0 to skip): ").strip())
                        if selection > 0 and selection <= len(world_files):
                            file_path = world_files[selection - 1]
                            if self.game_manager.upload_world_file(game_name, file_path):
                                print(f"\n[OK] World file uploaded successfully!")
                            else:
                                print(f"\n[ERROR] Failed to upload world file!")
                    except ValueError:
                        print("\n[ERROR] Invalid input!")
                else:
                    print("\n[ERROR] No .mcworld or .mctemplate files found in Downloads!")
        else:
            print(f"\n[ERROR] Game folder '{game_name}' already exists!")
        
        self.wait_for_key()
    
    def load_existing_game(self):
        """Load an existing game folder."""
        self.clear_screen()
        print("=" * 70)
        print("    LOAD EXISTING GAME")
        print("=" * 70)
        
        games = self.game_manager.list_games()
        
        if not games:
            print("\n[ERROR] No games found! Create a new game first.")
            self.wait_for_key()
            return
        
        print("\nAvailable games:")
        for i, game in enumerate(games, 1):
            marker = "→" if game == self.current_game else " "
            
            # Show brief status
            info = self.game_manager.load_game_info(game)
            status = []
            if info:
                if info.get("world_files"): status.append("W")
                if info.get("context"): status.append("C")
                if info.get("gameplay"): status.append("G")
                if info.get("objectives"): status.append("O")
            status_str = f"[{''.join(status)}]" if status else "[Empty]"
            
            print(f"{marker} {i}. {game} {status_str}")
        
        print("\n(W=World, C=Context, G=Gameplay, O=Objectives)")
        
        try:
            selection = int(input("\nSelect game number (0 to cancel): ").strip())
            if selection == 0:
                return
            if 1 <= selection <= len(games):
                self.current_game = games[selection - 1]
                print(f"\n[OK] Loaded game: {self.current_game}")
            else:
                print("\n[ERROR] Invalid selection!")
        except ValueError:
            print("\n[ERROR] Invalid input!")
        
        self.wait_for_key()
    
    def upload_world_file(self):
        """Upload a world file to the current game."""
        self.clear_screen()
        print("=" * 70)
        print(f"    UPLOAD WORLD FILE - {self.current_game}")
        print("=" * 70)
        
        world_files = self.game_manager.list_world_files_in_downloads()
        if world_files:
            print("\nAvailable world files in Downloads:")
            for i, file in enumerate(world_files, 1):
                filename = file.split('/')[-1]
                print(f"{i}. {filename}")
            
            try:
                selection = int(input("\nSelect file number (0 to cancel): ").strip())
                if selection == 0:
                    return
                elif 1 <= selection <= len(world_files):
                    file_path = world_files[selection - 1]
                    if self.game_manager.upload_world_file(self.current_game, file_path):
                        print(f"\n[OK] World file uploaded successfully!")
                        
                        # Prompt to extract lang files
                        extract = input("\nExtract language files now? (y/n): ").strip().lower()
                        if extract == 'y':
                            self.extract_lang_files()
                            return  # Don't wait for key as extract_lang_files does it
                    else:
                        print(f"\n[ERROR] Failed to upload world file!")
                else:
                    print("\n[ERROR] Invalid selection!")
            except ValueError:
                print("\n[ERROR] Invalid input!")
        else:
            print("\n[ERROR] No .mcworld or .mctemplate files found in Downloads!")
        
        self.wait_for_key()
    
    def load_create_game_old(self):
        """DEPRECATED: Old load/create method."""
        self.clear_screen()
        print("=" * 60)
        print("    LOAD/CREATE GAME FOLDER")
        print("=" * 60)
        
        print("\n1. Create new game folder")
        print("2. Create game folder and upload world file")
        print("3. Load existing game folder")
        print("4. Upload world file to current game")
        print("0. Back to main menu")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "1":
            game_name = input("\nEnter game name: ").strip()
            if game_name:
                result = self.game_manager.create_game_folder(game_name)
                if result:
                    self.current_game = game_name
                    print(f"\n[OK] Game folder '{game_name}' created successfully!")
                else:
                    print(f"\n[ERROR] Game folder '{game_name}' already exists!")
            else:
                print("\n[ERROR] Game name cannot be empty!")
            self.wait_for_key()
            
        elif choice == "2":
            game_name = input("\nEnter game name: ").strip()
            if game_name:
                result = self.game_manager.create_game_folder(game_name)
                if result:
                    self.current_game = game_name
                    print(f"\n[OK] Game folder '{game_name}' created successfully!")
                    
                    # Now upload world file
                    world_files = self.game_manager.list_world_files_in_downloads()
                    if world_files:
                        print("\nAvailable world files in Downloads:")
                        for i, file in enumerate(world_files, 1):
                            print(f"{i}. {file}")
                        
                        try:
                            selection = int(input("\nSelect file number (0 to skip): ").strip())
                            if selection == 0:
                                print("\nSkipped file upload.")
                            elif 1 <= selection <= len(world_files):
                                file_path = world_files[selection - 1]
                                if self.game_manager.upload_world_file(game_name, file_path):
                                    print(f"\n[OK] World file uploaded successfully!")
                                else:
                                    print(f"\n[ERROR] Failed to upload world file!")
                            else:
                                print("\n[ERROR] Invalid selection!")
                        except ValueError:
                            print("\n[ERROR] Invalid input!")
                    else:
                        print("\n[ERROR] No .mcworld or .mctemplate files found in Downloads!")
                else:
                    print(f"\n[ERROR] Game folder '{game_name}' already exists!")
            else:
                print("\n[ERROR] Game name cannot be empty!")
            self.wait_for_key()
            
        elif choice == "3":
            games = self.game_manager.list_games()
            if games:
                print("\nAvailable games:")
                for i, game in enumerate(games, 1):
                    print(f"{i}. {game}")
                
                try:
                    selection = int(input("\nSelect game number: ").strip())
                    if 1 <= selection <= len(games):
                        self.current_game = games[selection - 1]
                        print(f"\n[OK] Loaded game: {self.current_game}")
                    else:
                        print("\n[ERROR] Invalid selection!")
                except ValueError:
                    print("\n[ERROR] Invalid input!")
            else:
                print("\n[ERROR] No games found!")
            self.wait_for_key()
            
        elif choice == "4":
            if not self.current_game:
                print("\n[ERROR] Please load a game first!")
                self.wait_for_key()
                return
            
            world_files = self.game_manager.list_world_files_in_downloads()
            if world_files:
                print("\nAvailable world files in Downloads:")
                for i, file in enumerate(world_files, 1):
                    print(f"{i}. {file}")
                
                try:
                    selection = int(input("\nSelect file number (0 to cancel): ").strip())
                    if selection == 0:
                        return
                    elif 1 <= selection <= len(world_files):
                        file_path = world_files[selection - 1]
                        if self.game_manager.upload_world_file(self.current_game, file_path):
                            print(f"\n[OK] World file uploaded successfully!")
                        else:
                            print(f"\n[ERROR] Failed to upload world file!")
                    else:
                        print("\n[ERROR] Invalid selection!")
                except ValueError:
                    print("\n[ERROR] Invalid input!")
            else:
                print("\n[ERROR] No .mcworld or .mctemplate files found in Downloads!")
            self.wait_for_key()
    
    def add_game_context(self):
        """Option 2: Add game context."""
        if not self.current_game:
            print("\n[ERROR] Please load a game first!")
            self.wait_for_key()
            return
        
        self.clear_screen()
        print("=" * 60)
        print(f"    ADD GAME CONTEXT - {self.current_game}")
        print("=" * 60)
        
        # Check if context already exists
        existing_info = self.game_manager.load_game_info(self.current_game)
        existing_context = existing_info.get("context") if existing_info else None
        
        if existing_context:
            print("\n EXISTING CONTEXT:")
            print("-" * 60)
            print(existing_context)
            print("-" * 60)
            
            print("\n1. Replace with new context")
            print("2. Edit existing context")
            if self.settings.is_configured():
                print("3. Standardize with Azure OpenAI")
                print("4. Generate from Documents & Lang Analysis (AI)")
            print("0. Cancel")
            
            choice = input("\nEnter your choice: ").strip()
            
            if choice == "0":
                return
            elif choice == "2":
                print("\nEdit context (current context shown above):")
                print("Enter new text (Press Ctrl+D or Ctrl+Z when finished)")
                print("Leave empty to keep existing context.\n")
                
                lines = []
                try:
                    while True:
                        line = input()
                        lines.append(line)
                except EOFError:
                    pass
                
                new_context = "\n".join(lines).strip()
                context = new_context if new_context else existing_context
            elif choice == "3" and self.settings.is_configured():
                print("\n[AI] Standardizing context with Azure OpenAI...")
                standardized = self.game_manager.standardize_with_ai(existing_context, "context")
                if standardized:
                    print("\n STANDARDIZED CONTEXT:")
                    print("-" * 60)
                    print(standardized)
                    print("-" * 60)
                    
                    confirm = input("\nUse this standardized version? (y/n): ").strip().lower()
                    if confirm == 'y':
                        context = standardized
                        self.game_manager.save_game_info(self.current_game, "context", context)
                        print(f"\n[OK] Standardized context saved for '{self.current_game}'!")
                    else:
                        print("\n[ERROR] Standardization cancelled.")
                else:
                    print("\n[ERROR] Failed to standardize context.")
                self.wait_for_key()
                return
            elif choice == "4" and self.settings.is_configured():
                # Generate context from existing data sources
                print("\n Checking available data sources...")
                
                info = self.game_manager.load_game_info(self.current_game)
                metadata = self.game_manager._load_metadata(self.current_game)
                
                has_lang = info and info.get("lang_analysis")
                has_docs = info and info.get("document_analysis")
                
                if not has_lang and not has_docs:
                    print("\n[ERROR] No language file analysis or document analysis found!")
                    print("   Please upload a world file or documents first.")
                    self.wait_for_key()
                    return
                
                print("\n Using the following data sources:")
                if has_lang:
                    print("   [OK] Language File Analysis (NPC dialogue & narrative)")
                if has_docs:
                    doc_count = len(metadata.get("documents", []))
                    print(f"   [OK] Document Analysis ({doc_count} document(s))")
                
                confirm = input("\n Generate context from these sources? (y/n): ").strip().lower()
                if confirm != 'y':
                    print("\n[ERROR] Generation cancelled.")
                    self.wait_for_key()
                    return
                
                print("\n[AI] Generating context from available data...")
                generated = self.game_manager.generate_context_from_data(self.current_game)
                
                if generated:
                    print("\n GENERATED CONTEXT:")
                    print("-" * 60)
                    print(generated)
                    print("-" * 60)
                    
                    confirm = input("\nUse this generated context? (y/n): ").strip().lower()
                    if confirm == 'y':
                        context = generated
                        self.game_manager.save_game_info(self.current_game, "context", context)
                        print(f"\n[OK] Generated context saved for '{self.current_game}'!")
                    else:
                        print("\n[ERROR] Generation cancelled.")
                else:
                    print("\n[ERROR] Failed to generate context.")
                self.wait_for_key()
                return
            elif choice == "1":
                print("\nEnter new game context (educational background, theme, setting):")
                print("(Press Ctrl+D or Ctrl+Z when finished)\n")
                
                lines = []
                try:
                    while True:
                        line = input()
                        lines.append(line)
                except EOFError:
                    pass
                
                context = "\n".join(lines)
            else:
                print("\n[ERROR] Invalid choice!")
                self.wait_for_key()
                return
        else:
            # No existing context - offer to generate or manually enter
            if self.settings.is_configured():
                # Check if data sources are available
                info = self.game_manager.load_game_info(self.current_game)
                metadata = self.game_manager._load_metadata(self.current_game)
                has_lang = info and info.get("lang_analysis")
                has_docs = info and info.get("document_analysis")
                
                if has_lang or has_docs:
                    print("\n Data sources available for AI generation:")
                    if has_lang:
                        print("   [OK] Language File Analysis")
                    if has_docs:
                        doc_count = len(metadata.get("documents", []))
                        print(f"   [OK] Document Analysis ({doc_count} document(s))")
                    
                    print("\n1. Generate context from available data (AI)")
                    print("2. Enter context manually")
                    print("0. Cancel")
                    
                    choice = input("\nEnter your choice: ").strip()
                    
                    if choice == "0":
                        return
                    elif choice == "1":
                        print("\n[AI] Generating context from available data...")
                        generated = self.game_manager.generate_context_from_data(self.current_game)
                        
                        if generated:
                            print("\n GENERATED CONTEXT:")
                            print("-" * 60)
                            print(generated)
                            print("-" * 60)
                            
                            confirm = input("\nUse this generated context? (y/n): ").strip().lower()
                            if confirm == 'y':
                                context = generated
                                self.game_manager.save_game_info(self.current_game, "context", context)
                                print(f"\n[OK] Generated context saved for '{self.current_game}'!")
                                self.wait_for_key()
                                return
                            else:
                                print("\n[ERROR] Generation cancelled.")
                                self.wait_for_key()
                                return
                        else:
                            print("\n[ERROR] Failed to generate context.")
                            self.wait_for_key()
                            return
                    elif choice != "2":
                        print("\n[ERROR] Invalid choice!")
                        self.wait_for_key()
                        return
            
            print("\nEnter game context (educational background, theme, setting):")
            print("(Press Ctrl+D or Ctrl+Z when finished)\n")
            
            lines = []
            try:
                while True:
                    line = input()
                    lines.append(line)
            except EOFError:
                pass
            
            context = "\n".join(lines)
        
        if context.strip():
            # Option to use AI to enhance context
            if not existing_context or choice == "1":
                use_ai = input("\n\nUse Azure OpenAI to enhance context? (y/n): ").strip().lower()
                
                if use_ai == 'y' and self.settings.is_configured():
                    print("\n[AI] Enhancing context with AI...")
                    enhanced_context = self.game_manager.enhance_with_ai(context, "context")
                    if enhanced_context:
                        context = enhanced_context
                        print("[OK] Context enhanced!")
            
            self.game_manager.save_game_info(self.current_game, "context", context)
            print(f"\n[OK] Game context saved for '{self.current_game}'!")
        else:
            print("\n[ERROR] Context cannot be empty!")
        
        self.wait_for_key()
    
    def add_gameplay_description(self):
        """Option 3: Add gameplay description."""
        if not self.current_game:
            print("\n[ERROR] Please load a game first!")
            self.wait_for_key()
            return
        
        self.clear_screen()
        print("=" * 60)
        print(f"    ADD GAMEPLAY DESCRIPTION - {self.current_game}")
        print("=" * 60)
        
        # Check if gameplay description already exists
        existing_info = self.game_manager.load_game_info(self.current_game)
        existing_gameplay = existing_info.get("gameplay") if existing_info else None
        
        if existing_gameplay:
            print("\n EXISTING GAMEPLAY DESCRIPTION:")
            print("-" * 60)
            print(existing_gameplay)
            print("-" * 60)
            
            print("\n1. Replace with new description")
            print("2. Edit existing description")
            if self.settings.is_configured():
                print("3. Standardize with Azure OpenAI")
                print("4. Generate from Documents & Lang Analysis (AI)")
            print("0. Cancel")
            
            choice = input("\nEnter your choice: ").strip()
            
            if choice == "0":
                return
            elif choice == "2":
                print("\nEdit description (current description shown above):")
                print("Enter new text (Press Ctrl+D or Ctrl+Z when finished)")
                print("Leave empty to keep existing description.\n")
                
                lines = []
                try:
                    while True:
                        line = input()
                        lines.append(line)
                except EOFError:
                    pass
                
                new_description = "\n".join(lines).strip()
                description = new_description if new_description else existing_gameplay
            elif choice == "3" and self.settings.is_configured():
                print("\n[AI] Standardizing gameplay description with Azure OpenAI...")
                standardized = self.game_manager.standardize_with_ai(existing_gameplay, "gameplay")
                if standardized:
                    print("\n STANDARDIZED GAMEPLAY DESCRIPTION:")
                    print("-" * 60)
                    print(standardized)
                    print("-" * 60)
                    
                    confirm = input("\nUse this standardized version? (y/n): ").strip().lower()
                    if confirm == 'y':
                        description = standardized
                        self.game_manager.save_game_info(self.current_game, "gameplay", description)
                        print(f"\n[OK] Standardized gameplay description saved for '{self.current_game}'!")
                    else:
                        print("\n[ERROR] Standardization cancelled.")
                else:
                    print("\n[ERROR] Failed to standardize description.")
                self.wait_for_key()
                return
            elif choice == "4" and self.settings.is_configured():
                # Generate gameplay from existing data sources
                print("\n Checking available data sources...")
                
                info = self.game_manager.load_game_info(self.current_game)
                metadata = self.game_manager._load_metadata(self.current_game)
                
                has_lang = info and info.get("lang_analysis")
                has_docs = info and info.get("document_analysis")
                
                if not has_lang and not has_docs:
                    print("\n[ERROR] No language file analysis or document analysis found!")
                    print("   Please upload a world file or documents first.")
                    self.wait_for_key()
                    return
                
                print("\n Using the following data sources:")
                if has_lang:
                    print("   [OK] Language File Analysis (NPC dialogue & narrative)")
                if has_docs:
                    doc_count = len(metadata.get("documents", []))
                    print(f"   [OK] Document Analysis ({doc_count} document(s))")
                
                confirm = input("\nGenerate gameplay description from these sources? (y/n): ").strip().lower()
                if confirm != 'y':
                    print("\n[ERROR] Generation cancelled.")
                    self.wait_for_key()
                    return
                
                print("\n[AI] Generating gameplay description from available data...")
                generated = self.game_manager.generate_gameplay_from_data(self.current_game)
                
                if generated:
                    print("\n GENERATED GAMEPLAY DESCRIPTION:")
                    print("-" * 60)
                    print(generated)
                    print("-" * 60)
                    
                    confirm = input("\nUse this generated gameplay description? (y/n): ").strip().lower()
                    if confirm == 'y':
                        description = generated
                        self.game_manager.save_game_info(self.current_game, "gameplay", description)
                        print(f"\n[OK] Generated gameplay description saved for '{self.current_game}'!")
                    else:
                        print("\n[ERROR] Generation cancelled.")
                else:
                    print("\n[ERROR] Failed to generate gameplay description.")
                self.wait_for_key()
                return
            elif choice == "1":
                print("\nEnter new gameplay description (mechanics, objectives, player actions):")
                print("(Press Ctrl+D or Ctrl+Z when finished)\n")
                
                lines = []
                try:
                    while True:
                        line = input()
                        lines.append(line)
                except EOFError:
                    pass
                
                description = "\n".join(lines)
            else:
                print("\n[ERROR] Invalid choice!")
                self.wait_for_key()
                return
        else:
            # No existing gameplay - offer to generate or manually enter
            if self.settings.is_configured():
                # Check if data sources are available
                info = self.game_manager.load_game_info(self.current_game)
                metadata = self.game_manager._load_metadata(self.current_game)
                has_lang = info and info.get("lang_analysis")
                has_docs = info and info.get("document_analysis")
                
                if has_lang or has_docs:
                    print("\n Data sources available for AI generation:")
                    if has_lang:
                        print("   [OK] Language File Analysis")
                    if has_docs:
                        doc_count = len(metadata.get("documents", []))
                        print(f"   [OK] Document Analysis ({doc_count} document(s))")
                    
                    print("\n1. Generate gameplay description from available data (AI)")
                    print("2. Enter gameplay description manually")
                    print("0. Cancel")
                    
                    choice = input("\nEnter your choice: ").strip()
                    
                    if choice == "0":
                        return
                    elif choice == "1":
                        print("\n[AI] Generating gameplay description from available data...")
                        generated = self.game_manager.generate_gameplay_from_data(self.current_game)
                        
                        if generated:
                            print("\n GENERATED GAMEPLAY DESCRIPTION:")
                            print("-" * 60)
                            print(generated)
                            print("-" * 60)
                            
                            confirm = input("\nUse this generated gameplay description? (y/n): ").strip().lower()
                            if confirm == 'y':
                                description = generated
                                self.game_manager.save_game_info(self.current_game, "gameplay", description)
                                print(f"\n[OK] Generated gameplay description saved for '{self.current_game}'!")
                                self.wait_for_key()
                                return
                            else:
                                print("\n[ERROR] Generation cancelled.")
                                self.wait_for_key()
                                return
                        else:
                            print("\n[ERROR] Failed to generate gameplay description.")
                            self.wait_for_key()
                            return
                    elif choice != "2":
                        print("\n[ERROR] Invalid choice!")
                        self.wait_for_key()
                        return
            
            print("\nEnter gameplay description (mechanics, objectives, player actions):")
            print("(Press Ctrl+D or Ctrl+Z when finished)\n")
            
            lines = []
            try:
                while True:
                    line = input()
                    lines.append(line)
            except EOFError:
                pass
            
            description = "\n".join(lines)
        
        if description.strip():
            if not existing_gameplay or choice == "1":
                use_ai = input("\n\nUse Azure OpenAI to enhance description? (y/n): ").strip().lower()
                
                if use_ai == 'y' and self.settings.is_configured():
                    print("\n[AI] Enhancing description with AI...")
                    enhanced_description = self.game_manager.enhance_with_ai(description, "gameplay")
                    if enhanced_description:
                        description = enhanced_description
                        print("[OK] Description enhanced!")
            
            self.game_manager.save_game_info(self.current_game, "gameplay", description)
            print(f"\n[OK] Gameplay description saved for '{self.current_game}'!")
        else:
            print("\n[ERROR] Description cannot be empty!")
        
        self.wait_for_key()
    
    def add_learning_objectives(self):
        """Option 4: Add learning objectives."""
        if not self.current_game:
            print("\n[ERROR] Please load a game first!")
            self.wait_for_key()
            return
        
        self.clear_screen()
        print("=" * 60)
        print(f"    ADD LEARNING OBJECTIVES - {self.current_game}")
        print("=" * 60)
        
        # Check if objectives already exist
        existing_info = self.game_manager.load_game_info(self.current_game)
        existing_objectives = existing_info.get("objectives") if existing_info else None
        
        if existing_objectives:
            print("\n EXISTING LEARNING OBJECTIVES:")
            print("-" * 60)
            if isinstance(existing_objectives, list):
                for i, obj in enumerate(existing_objectives, 1):
                    print(f"{i}. {obj}")
            else:
                print(existing_objectives)
            print("-" * 60)
            
            print("\n1. Replace with new objectives")
            print("2. Edit existing objectives")
            if self.settings.is_configured():
                print("3. Standardize with Azure OpenAI")
            print("0. Cancel")
            
            choice = input("\nEnter your choice: ").strip()
            
            if choice == "0":
                return
            elif choice == "2":
                print("\nEdit objectives (current objectives shown above):")
                print("Enter new objectives, one per line (Press Ctrl+D or Ctrl+Z when finished)")
                print("Leave empty to keep existing objectives.\n")
                
                new_objectives = []
                try:
                    while True:
                        line = input()
                        if line.strip():
                            new_objectives.append(line.strip())
                except EOFError:
                    pass
                
                objectives = new_objectives if new_objectives else existing_objectives
            elif choice == "3" and self.settings.is_configured():
                print("\n[AI] Standardizing learning objectives with Azure OpenAI...")
                obj_text = "\n".join(existing_objectives) if isinstance(existing_objectives, list) else existing_objectives
                standardized = self.game_manager.standardize_with_ai(obj_text, "objectives")
                if standardized:
                    # Parse objectives, removing common formatting (bullets, numbers, etc.)
                    standardized_list = []
                    for line in standardized.split("\n"):
                        line = line.strip()
                        if line:
                            # Remove common list markers: bullets, numbers, dashes
                            line = line.lstrip('•●○-*')
                            line = line.strip()
                            # Remove numbered list format (1. 2. etc.)
                            import re
                            line = re.sub(r'^\d+\.\s*', '', line)
                            line = re.sub(r'^[a-z]\)\s*', '', line, flags=re.IGNORECASE)
                            if line and len(line) > 10:  # Only keep substantial lines
                                standardized_list.append(line)
                    print("\n STANDARDIZED LEARNING OBJECTIVES:")
                    print("-" * 60)
                    for i, obj in enumerate(standardized_list, 1):
                        print(f"{i}. {obj}")
                    print("-" * 60)
                    
                    confirm = input("\nUse these standardized objectives? (y/n): ").strip().lower()
                    if confirm == 'y':
                        objectives = standardized_list
                        self.game_manager.save_game_info(self.current_game, "objectives", objectives)
                        print(f"\n[OK] Standardized learning objectives saved for '{self.current_game}'!")
                    else:
                        print("\n[ERROR] Standardization cancelled.")
                else:
                    print("\n[ERROR] Failed to standardize objectives.")
                self.wait_for_key()
                return
            elif choice == "1":
                print("\nEnter new learning objectives (one per line):")
                print("(Press Ctrl+D or Ctrl+Z when finished)\n")
                
                objectives = []
                try:
                    while True:
                        line = input()
                        if line.strip():
                            objectives.append(line.strip())
                except EOFError:
                    pass
            else:
                print("\n[ERROR] Invalid choice!")
                self.wait_for_key()
                return
        else:
            print("\nEnter learning objectives (one per line):")
            print("(Press Ctrl+D or Ctrl+Z when finished)\n")
            
            objectives = []
            try:
                while True:
                    line = input()
                    if line.strip():
                        objectives.append(line.strip())
            except EOFError:
                pass
        
        if objectives:
            if not existing_objectives or choice == "1":
                use_ai = input("\n\nUse Azure OpenAI to refine objectives? (y/n): ").strip().lower()
                
                if use_ai == 'y' and self.settings.is_configured():
                    print("\n[AI] Refining objectives with AI...")
                    objectives_text = "\n".join(objectives)
                    enhanced_objectives = self.game_manager.enhance_with_ai(objectives_text, "objectives")
                    if enhanced_objectives:
                        # Parse objectives, removing common formatting (bullets, numbers, etc.)
                        objectives = []
                        for line in enhanced_objectives.split("\n"):
                            line = line.strip()
                            if line:
                                # Remove common list markers: bullets, numbers, dashes
                                line = line.lstrip('•●○-*')
                                line = line.strip()
                                # Remove numbered list format (1. 2. etc.)
                                import re
                                line = re.sub(r'^\d+\.\s*', '', line)
                                line = re.sub(r'^[a-z]\)\s*', '', line, flags=re.IGNORECASE)
                                if line and len(line) > 10:  # Only keep substantial lines
                                    objectives.append(line)
                        print("[OK] Objectives refined!")
            
            self.game_manager.save_game_info(self.current_game, "objectives", objectives)
            print(f"\n[OK] Learning objectives saved for '{self.current_game}'!")
        else:
            print("\n[ERROR] No objectives entered!")
        
        self.wait_for_key()
    
    def extract_lang_files(self):
        """Option 5: Extract language files from uploaded game."""
        if not self.current_game:
            print("\n[ERROR] Please load a game first!")
            self.wait_for_key()
            return
        
        self.clear_screen()
        print("=" * 60)
        print(f"    EXTRACT LANGUAGE FILES - {self.current_game}")
        print("=" * 60)
        
        # Check if game has uploaded world files
        info = self.game_manager.load_game_info(self.current_game)
        if not info or "world_files" not in info or not info["world_files"]:
            print("\n[ERROR] No world files found! Please upload a game file first.")
            self.wait_for_key()
            return
        
        print("\nSearching for language files in uploaded world files...\n")
        
        result = self.game_manager.extract_lang_files(self.current_game)
        
        if result and result["success"]:
            print(f"\n[OK] Language file extracted successfully!")
            print(f"\nLanguage: {result['language']}")
            print(f"File Path in Archive: {result.get('file_path', 'N/A')}")
            print(f"Total entries: {result['entry_count']}")
            print(f"NPC Content Score: {result.get('score', 0)}")
            print(f"Analyzed {result.get('selected_from', 1)} candidate file(s)")
            
            if result['preview']:
                print("\n Preview (first 10 entries):")
                print("-" * 60)
                for key, value in list(result['preview'].items())[:10]:
                    # Truncate long values for preview
                    display_value = value if len(value) <= 80 else value[:77] + "..."
                    print(f"{key}: {display_value}")
                print("-" * 60)
            
            # Option to analyze with AI
            if self.settings.is_configured():
                analyze = input("\nAnalyze language file with Azure OpenAI? (y/n): ").strip().lower()
                if analyze == 'y':
                    print("\n[AI] Analyzing language file...")
                    analysis = self.game_manager.analyze_lang_file_with_ai(self.current_game)
                    if analysis:
                        print("\n ANALYSIS:")
                        print("-" * 60)
                        print(analysis)
                        print("-" * 60)
                        print("\n[OK] Analysis saved to game folder!")
        else:
            error_msg = result.get("error", "Unknown error") if result else "Failed to extract language files"
            print(f"\n[ERROR] {error_msg}")
        
        self.wait_for_key()
    
    def view_game_info(self):
        """View complete game information."""
        if not self.current_game:
            print("\n[ERROR] Please load a game first!")
            self.wait_for_key()
            return
        
        self.clear_screen()
        print("=" * 70)
        print(f"    GAME INFORMATION - {self.current_game}")
        print("=" * 70)
        
        info = self.game_manager.load_game_info(self.current_game)
        
        if info:
            if "world_files" in info and info["world_files"]:
                print("\n WORLD FILES:")
                print("-" * 60)
                for i, wf in enumerate(info["world_files"], 1):
                    print(f"{i}. {wf['filename']}")
                    print(f"   Uploaded: {wf['uploaded']}")
            
            # Load metadata to check for lang file and documents
            metadata = self.game_manager._load_metadata(self.current_game)
            if metadata and "lang_file" in metadata:
                print("\n🌐 LANGUAGE FILE:")
                print("-" * 60)
                lang_info = metadata["lang_file"]
                print(f"Language: {lang_info['filename'].replace('.lang', '')}")
                print(f"Entries: {lang_info['entry_count']}")
                print(f"Extracted: {lang_info['extracted']}")
                if lang_info.get('ai_analyzed'):
                    print(f"AI Analysis: [OK]")
            
            if metadata and "documents" in metadata and metadata["documents"]:
                print("\n UPLOADED DOCUMENTS:")
                print("-" * 60)
                for doc in metadata["documents"]:
                    print(f"• {doc['filename']}")
                    print(f"  Type: {doc['type']} | Uploaded: {doc['uploaded'][:10]}")
                    if doc.get('ai_analyzed'):
                        print(f"  AI Analysis: [OK]")
            
            if "lang_analysis" in info:
                print("\n[AI] LANGUAGE FILE AI ANALYSIS:")
                print("-" * 60)
                analysis = info["lang_analysis"]
                # Show summary or full analysis
                if isinstance(analysis, dict) and "summary" in analysis:
                    print(analysis["summary"])
                else:
                    print(str(analysis)[:500] + "..." if len(str(analysis)) > 500 else str(analysis))
            
            if "document_analysis" in info and info["document_analysis"]:
                print("\n DOCUMENT ANALYSIS:")
                print("-" * 60)
                doc_analyses = info["document_analysis"]
                if isinstance(doc_analyses, dict):
                    for doc_name, doc_data in doc_analyses.items():
                        print(f"\n {doc_name}")
                        if isinstance(doc_data, dict) and "summary" in doc_data:
                            print(f"   {doc_data['summary'][:200]}...")
                        print()
            
            if "context" in info:
                print("\n CONTEXT:")
                print("-" * 60)
                print(info["context"])
            
            if "gameplay" in info:
                print("\n GAMEPLAY DESCRIPTION:")
                print("-" * 60)
                print(info["gameplay"])
            
            if "objectives" in info:
                print("\n LEARNING OBJECTIVES:")
                print("-" * 60)
                if isinstance(info["objectives"], list):
                    for i, obj in enumerate(info["objectives"], 1):
                        print(f"{i}. {obj}")
                else:
                    print(info["objectives"])
        else:
            print("\n[ERROR] No information found for this game.")
        
        self.wait_for_key()
    
    def list_all_games(self):
        """List all games with detailed status."""
        self.clear_screen()
        print("=" * 70)
        print("    ALL GAMES")
        print("=" * 70)
        
        games = self.game_manager.list_games()
        
        if games:
            print(f"\nTotal games: {len(games)}\n")
            
            for i, game in enumerate(games, 1):
                marker = "→" if game == self.current_game else " "
                
                # Get detailed status
                info = self.game_manager.load_game_info(game)
                metadata = self.game_manager._load_metadata(game)
                
                status_parts = []
                if info:
                    if info.get("world_files"): 
                        world_count = len(info["world_files"])
                        status_parts.append(f"{world_count} world file(s)")
                    if info.get("context"): status_parts.append("Context")
                    if info.get("gameplay"): status_parts.append("Gameplay")
                    if info.get("objectives"): status_parts.append("Objectives")
                    if metadata and metadata.get("lang_file"): status_parts.append("Lang file")
                    if info.get("lang_analysis"): status_parts.append("AI analyzed")
                
                status_str = " | ".join(status_parts) if status_parts else "Empty"
                
                print(f"{marker} {i}. {game}")
                print(f"     {status_str}")
                
                # Show modified date if available
                if metadata and metadata.get("modified"):
                    modified = metadata["modified"][:10]  # Just the date part
                    print(f"     Last modified: {modified}")
                print()
            
            # Option to load a game
            load = input("Enter game number to load (Enter to return): ").strip()
            if load.isdigit():
                selection = int(load)
                if 1 <= selection <= len(games):
                    self.current_game = games[selection - 1]
                    print(f"\n[OK] Loaded game: {self.current_game}")
                    self.wait_for_key()
        else:
            print("\n[ERROR] No games found!")
            self.wait_for_key()
    
    def upload_analyze_documents(self):
        """Upload and analyze supporting documents (PDF, Word, PPT)."""
        self.clear_screen()
        print("=" * 70)
        print(f"    UPLOAD & ANALYZE DOCUMENTS - {self.current_game}")
        print("=" * 70)
        
        print("\nSupported formats: PDF, Word (.docx), PowerPoint (.pptx)")
        print("\nSearching Downloads folder...\n")
        
        documents = self.game_manager.list_documents_in_downloads()
        
        if not documents:
            print("\n[ERROR] No supported documents found in Downloads folder!")
            self.wait_for_key()
            return
        
        print("Available documents:")
        for i, doc_path in enumerate(documents, 1):
            filename = doc_path.split('/')[-1]
            print(f"{i}. {filename}")
        
        try:
            selection = int(input("\nSelect document number (0 to cancel): ").strip())
            if selection == 0:
                return
            elif 1 <= selection <= len(documents):
                doc_path = documents[selection - 1]
                filename = doc_path.split('/')[-1]
                
                print(f"\n Uploading {filename}...")
                upload_result = self.game_manager.upload_document(self.current_game, doc_path)
                
                if upload_result:
                    print(f"[OK] Document uploaded successfully!")
                    
                    # Automatically analyze with AI if configured
                    if self.settings.is_configured():
                        print("\n[AI] Automatically analyzing document...")
                        analysis = self.game_manager.analyze_document_with_ai(self.current_game, filename)
                        
                        if analysis:
                            print("[OK] Document analysis complete!")
                            print("\n DOCUMENT ANALYSIS (Preview):")
                            print("-" * 70)
                            # Show first 300 characters of analysis
                            preview = analysis[:300] + "..." if len(analysis) > 300 else analysis
                            print(preview)
                            print("-" * 70)
                            print("\n[OK] Full analysis saved to game folder!")
                        else:
                            print("[ERROR] Failed to analyze document.")
                    else:
                        print("\n⚠ Azure OpenAI not configured. Document uploaded but not analyzed.")
                        print("   Configure Azure OpenAI in Settings to enable automatic analysis.")
                else:
                    print(f"\n[ERROR] Failed to upload document!")
            else:
                print("\n[ERROR] Invalid selection!")
        except ValueError:
            print("\n[ERROR] Invalid input!")
        
        self.wait_for_key()
    
    def export_game_info(self):
        """Export game information to markdown."""
        if not self.current_game:
            print("\n[ERROR] Please load a game first!")
            self.wait_for_key()
            return
        
        self.clear_screen()
        print("=" * 70)
        print(f"    EXPORT GAME INFORMATION - {self.current_game}")
        print("=" * 70)
        
        result = self.game_manager.export_game(self.current_game)
        
        if result:
            print(f"\n[OK] Game information exported to: {result}")
        else:
            print("\n[ERROR] Failed to export game information!")
        
        self.wait_for_key()
    
    def export_all_creations(self):
        """Export all created resources to a single folder."""
        if not self.current_game:
            print("\n[ERROR] Please load a game first!")
            self.wait_for_key()
            return
        
        self.clear_screen()
        print("=" * 70)
        print(f"    EXPORT ALL CREATIONS - {self.current_game}")
        print("=" * 70)
        
        # Ask for export format
        print("\nSelect export format:")
        print("  1. Markdown (.md) - Text format, editable")
        print("  2. Word Document (.docx) - Microsoft Word format")
        print("  3. PDF (.pdf) - Portable Document Format")
        print("  0. Cancel")
        
        format_choice = input("\nEnter choice (1-3): ").strip()
        
        format_map = {
            '1': 'md',
            '2': 'docx',
            '3': 'pdf'
        }
        
        if format_choice == '0':
            return
        
        export_format = format_map.get(format_choice, 'md')
        
        if format_choice not in format_map:
            print("\n[WARNING]  Invalid choice, defaulting to Markdown format")
            export_format = 'md'
        
        print(f"\n Exporting in {export_format.upper()} format...")
        
        result = self.game_manager.export_all_creations(self.current_game, export_format)
        
        if result:
            print(f"\n[OK] All creations exported successfully!")
            print(f"\n Export folder: {result['folder']}")
            print(f"\n Files exported:")
            print("-" * 70)
            if result['files']:
                for file in result['files']:
                    print(f"  [OK] {file}")
                print("-" * 70)
                print(f"\nTotal: {len(result['files'])} file(s)")
                
                # Ask if user wants to open the folder
                open_folder = input("\n\nOpen folder in Finder? (y/n): ").strip().lower()
                if open_folder == 'y':
                    try:
                        import subprocess
                        import platform
                        
                        system = platform.system()
                        if system == 'Darwin':  # macOS
                            subprocess.run(['open', result['folder']])
                            print("\n[OK] Opening folder in Finder...")
                        elif system == 'Windows':
                            subprocess.run(['explorer', result['folder']])
                            print("\n[OK] Opening folder in Explorer...")
                        else:  # Linux
                            subprocess.run(['xdg-open', result['folder']])
                            print("\n[OK] Opening folder...")
                    except Exception as e:
                        print(f"\n[ERROR] Could not open folder: {e}")
            else:
                print("  No creation files found.")
                print("  Create resources using the CREATION menu first.")
        else:
            print("\n[ERROR] Failed to export creations!")
        
        self.wait_for_key()
    
    def remove_documents(self):
        """Remove uploaded documents and their analysis."""
        self.clear_screen()
        print("=" * 70)
        print(f"    REMOVE DOCUMENTS - {self.current_game}")
        print("=" * 70)
        
        metadata = self.game_manager._load_metadata(self.current_game)
        
        if not metadata or "documents" not in metadata or not metadata["documents"]:
            print("\n[ERROR] No documents found for this game.")
            self.wait_for_key()
            return
        
        documents = metadata["documents"]
        
        print("\nUploaded documents:")
        print("-" * 70)
        for i, doc in enumerate(documents, 1):
            status = "[OK] Analyzed" if doc.get("ai_analyzed") else "Not analyzed"
            print(f"{i}. {doc['filename']}")
            print(f"   Type: {doc['type']} | Uploaded: {doc['uploaded'][:10]} | {status}")
        print("-" * 70)
        
        print("\nOptions:")
        print("  Enter document number to remove")
        print("  'all' to remove all documents")
        print("  '0' to cancel")
        
        choice = input("\nYour choice: ").strip().lower()
        
        if choice == "0":
            return
        elif choice == "all":
            confirm = input(f"\nRemove ALL {len(documents)} document(s) and their analysis? (yes/no): ").strip().lower()
            if confirm == "yes":
                result = self.game_manager.remove_all_documents(self.current_game)
                if result:
                    print(f"\n[OK] All documents and analysis removed successfully!")
                else:
                    print("\n[ERROR] Failed to remove documents.")
            else:
                print("\n[ERROR] Cancelled.")
        else:
            try:
                doc_num = int(choice)
                if 1 <= doc_num <= len(documents):
                    doc_to_remove = documents[doc_num - 1]
                    confirm = input(f"\nRemove '{doc_to_remove['filename']}' and its analysis? (y/n): ").strip().lower()
                    if confirm == 'y':
                        result = self.game_manager.remove_document(self.current_game, doc_to_remove['filename'])
                        if result:
                            print(f"\n[OK] Document and analysis removed successfully!")
                        else:
                            print("\n[ERROR] Failed to remove document.")
                    else:
                        print("\n[ERROR] Cancelled.")
                else:
                    print("\n[ERROR] Invalid document number!")
            except ValueError:
                print("\n[ERROR] Invalid input!")
        
        self.wait_for_key()
    
    def create_student_guide(self):
        """Create a student guide using all available game information."""
        if not self.settings.is_configured():
            print("\n[ERROR] Azure OpenAI must be configured to use creation features!")
            self.wait_for_key()
            return
        
        self.clear_screen()
        print("=" * 70)
        print(f"    CREATE STUDENT GUIDE - {self.current_game}")
        print("=" * 70)
        
        print("\n Generating comprehensive student guide...\n")
        
        # Show what information is available
        info = self.game_manager.load_game_info(self.current_game)
        metadata = self.game_manager._load_metadata(self.current_game)
        
        print(" Using the following information:")
        print("-" * 70)
        if info and info.get("context"):
            print("[OK] Game Context")
        if info and info.get("gameplay"):
            print("[OK] Gameplay Description")
        if info and info.get("objectives"):
            obj_count = len(info["objectives"]) if isinstance(info["objectives"], list) else 1
            print(f"[OK] Learning Objectives ({obj_count} objectives)")
        if info and info.get("lang_analysis"):
            print("[OK] Language File Analysis (NPC dialogue & narrative)")
        if info and info.get("document_analysis"):
            doc_count = len(info["document_analysis"]) if isinstance(info["document_analysis"], dict) else 1
            print(f"[OK] Document Analysis ({doc_count} document(s))")
        if metadata and metadata.get("world_files"):
            print("[OK] World File Information")
        print("-" * 70)
        print("\n⏳ Processing...\n")
        
        result = self.game_manager.create_student_guide(self.current_game)
        
        if result:
            print(f"\n[OK] Student guide created successfully!")
            print(f"\n Saved to: {result}")
            
            # Ask if user wants to view it
            view = input("\nView the guide now? (y/n): ").strip().lower()
            if view == 'y':
                self.clear_screen()
                try:
                    with open(result, 'r', encoding='utf-8') as f:
                        print(f.read())
                except Exception as e:
                    print(f"Error reading file: {e}")
        else:
            print("\n[ERROR] Failed to create student guide.")
        
        self.wait_for_key()
    
    def create_student_workbook(self):
        """Create a student workbook with activities and exercises."""
        if not self.settings.is_configured():
            print("\n[ERROR] Azure OpenAI must be configured to use creation features!")
            self.wait_for_key()
            return
        
        self.clear_screen()
        print("=" * 70)
        print(f"    CREATE STUDENT WORKBOOK - {self.current_game}")
        print("=" * 70)
        
        print("\n Generating interactive student workbook...\n")
        
        # Show what information is available
        info = self.game_manager.load_game_info(self.current_game)
        metadata = self.game_manager._load_metadata(self.current_game)
        
        print(" Using the following information:")
        print("-" * 70)
        if info and info.get("context"):
            print("[OK] Game Context")
        if info and info.get("gameplay"):
            print("[OK] Gameplay Description")
        if info and info.get("objectives"):
            obj_count = len(info["objectives"]) if isinstance(info["objectives"], list) else 1
            print(f"[OK] Learning Objectives ({obj_count} objectives)")
        if info and info.get("lang_analysis"):
            print("[OK] Language File Analysis (NPC dialogue & narrative)")
        if info and info.get("document_analysis"):
            doc_count = len(info["document_analysis"]) if isinstance(info["document_analysis"], dict) else 1
            print(f"[OK] Document Analysis ({doc_count} document(s))")
        if metadata and metadata.get("world_files"):
            print("[OK] World File Information")
        print("-" * 70)
        print("\n⏳ Processing...\n")
        
        result = self.game_manager.create_student_workbook(self.current_game)
        
        if result:
            print(f"\n[OK] Student workbook created successfully!")
            print(f"\n Saved to: {result}")
            
            # Ask if user wants to view it
            view = input("\nView the workbook now? (y/n): ").strip().lower()
            if view == 'y':
                self.clear_screen()
                try:
                    with open(result, 'r', encoding='utf-8') as f:
                        print(f.read())
                except Exception as e:
                    print(f"Error reading file: {e}")
        else:
            print("\n[ERROR] Failed to create student workbook.")
        
        self.wait_for_key()
    
    def create_student_quiz(self):
        """Create a student quiz with answers."""
        if not self.settings.is_configured():
            print("\n[ERROR] Azure OpenAI must be configured to use creation features!")
            self.wait_for_key()
            return
        
        self.clear_screen()
        print("=" * 70)
        print(f"    CREATE STUDENT QUIZ - {self.current_game}")
        print("=" * 70)
        
        print("\n Generating student quiz with answer key...\n")
        
        # Show what information is available
        info = self.game_manager.load_game_info(self.current_game)
        metadata = self.game_manager._load_metadata(self.current_game)
        
        print(" Using the following information:")
        print("-" * 70)
        if info and info.get("context"):
            print("[OK] Game Context")
        if info and info.get("gameplay"):
            print("[OK] Gameplay Description")
        if info and info.get("objectives"):
            obj_count = len(info["objectives"]) if isinstance(info["objectives"], list) else 1
            print(f"[OK] Learning Objectives ({obj_count} objectives)")
        if info and info.get("lang_analysis"):
            print("[OK] Language File Analysis (NPC dialogue & narrative)")
        if info and info.get("document_analysis"):
            doc_count = len(info["document_analysis"]) if isinstance(info["document_analysis"], dict) else 1
            print(f"[OK] Document Analysis ({doc_count} document(s))")
        if metadata and metadata.get("world_files"):
            print("[OK] World File Information")
        print("-" * 70)
        print("\n⏳ Processing...\n")
        
        result = self.game_manager.create_student_quiz(self.current_game)
        
        if result:
            print(f"\n[OK] Student quiz created successfully!")
            print(f"\n Quiz saved to: {result['quiz']}")
            print(f" Answer key saved to: {result['answers']}")
            
            # Ask if user wants to view it
            view = input("\nView the quiz now? (y/n): ").strip().lower()
            if view == 'y':
                self.clear_screen()
                print("=" * 70)
                print("STUDENT QUIZ")
                print("=" * 70)
                try:
                    with open(result['quiz'], 'r', encoding='utf-8') as f:
                        print(f.read())
                    
                    print("\n" + "=" * 70)
                    print("ANSWER KEY")
                    print("=" * 70)
                    with open(result['answers'], 'r', encoding='utf-8') as f:
                        print(f.read())
                except Exception as e:
                    print(f"Error reading file: {e}")
        else:
            print("\n[ERROR] Failed to create student quiz.")
        
        self.wait_for_key()
    
    def create_parent_guide(self):
        """Create a parent guide."""
        if not self.settings.is_configured():
            print("\n[ERROR] Azure OpenAI must be configured to use creation features!")
            self.wait_for_key()
            return
        
        self.clear_screen()
        print("=" * 70)
        print(f"    CREATE PARENT GUIDE - {self.current_game}")
        print("=" * 70)
        
        print("\n Generating parent guide...\n")
        
        # Show what information is available
        info = self.game_manager.load_game_info(self.current_game)
        metadata = self.game_manager._load_metadata(self.current_game)
        
        print(" Using the following information:")
        print("-" * 70)
        if info and info.get("context"):
            print("[OK] Game Context")
        if info and info.get("gameplay"):
            print("[OK] Gameplay Description")
        if info and info.get("objectives"):
            obj_count = len(info["objectives"]) if isinstance(info["objectives"], list) else 1
            print(f"[OK] Learning Objectives ({obj_count} objectives)")
        if info and info.get("lang_analysis"):
            print("[OK] Language File Analysis (NPC dialogue & narrative)")
        if info and info.get("document_analysis"):
            doc_count = len(info["document_analysis"]) if isinstance(info["document_analysis"], dict) else 1
            print(f"[OK] Document Analysis ({doc_count} document(s))")
        if metadata and metadata.get("world_files"):
            print("[OK] World File Information")
        print("-" * 70)
        print("\n⏳ Processing...\n")
        
        result = self.game_manager.create_parent_guide(self.current_game)
        
        if result:
            print(f"\n[OK] Parent guide created successfully!")
            print(f"\n Saved to: {result}")
            
            # Ask if user wants to view it
            view = input("\nView the guide now? (y/n): ").strip().lower()
            if view == 'y':
                self.clear_screen()
                print("=" * 70)
                print("PARENT GUIDE")
                print("=" * 70)
                try:
                    with open(result, 'r', encoding='utf-8') as f:
                        print(f.read())
                except Exception as e:
                    print(f"Error reading file: {e}")
        else:
            print("\n[ERROR] Failed to create parent guide.")
        
        self.wait_for_key()
    
    def create_teacher_guide(self):
        """Create a teacher guide."""
        if not self.settings.is_configured():
            print("\n[ERROR] Azure OpenAI must be configured to use creation features!")
            self.wait_for_key()
            return
        
        self.clear_screen()
        print("=" * 70)
        print(f"    CREATE TEACHER GUIDE - {self.current_game}")
        print("=" * 70)
        
        print("\n Generating teacher guide...\n")
        
        # Show what information is available
        info = self.game_manager.load_game_info(self.current_game)
        metadata = self.game_manager._load_metadata(self.current_game)
        
        print(" Using the following information:")
        print("-" * 70)
        if info and info.get("context"):
            print("[OK] Game Context")
        if info and info.get("gameplay"):
            print("[OK] Gameplay Description")
        if info and info.get("objectives"):
            obj_count = len(info["objectives"]) if isinstance(info["objectives"], list) else 1
            print(f"[OK] Learning Objectives ({obj_count} objectives)")
        if info and info.get("lang_analysis"):
            print("[OK] Language File Analysis (NPC dialogue & narrative)")
        if info and info.get("document_analysis"):
            doc_count = len(info["document_analysis"]) if isinstance(info["document_analysis"], dict) else 1
            print(f"[OK] Document Analysis ({doc_count} document(s))")
        if metadata and metadata.get("world_files"):
            print("[OK] World File Information")
        print("-" * 70)
        print("\n⏳ Processing...\n")
        
        result = self.game_manager.create_teacher_guide(self.current_game)
        
        if result:
            print(f"\n[OK] Teacher guide created successfully!")
            print(f"\n Saved to: {result}")
            
            # Ask if user wants to view it
            view = input("\nView the guide now? (y/n): ").strip().lower()
            if view == 'y':
                self.clear_screen()
                print("=" * 70)
                print("TEACHER GUIDE")
                print("=" * 70)
                try:
                    with open(result, 'r', encoding='utf-8') as f:
                        print(f.read())
                except Exception as e:
                    print(f"Error reading file: {e}")
        else:
            print("\n[ERROR] Failed to create teacher guide.")
        
        self.wait_for_key()
    
    def create_leadership_sheet(self):
        """Create a school leadership information sheet."""
        if not self.settings.is_configured():
            print("\n[ERROR] Azure OpenAI must be configured to use creation features!")
            self.wait_for_key()
            return
        
        self.clear_screen()
        print("=" * 70)
        print(f"    CREATE SCHOOL LEADERSHIP INFO SHEET - {self.current_game}")
        print("=" * 70)
        
        print("\n Generating leadership information sheet...\n")
        
        # Show what information is available
        info = self.game_manager.load_game_info(self.current_game)
        metadata = self.game_manager._load_metadata(self.current_game)
        
        print(" Using the following information:")
        print("-" * 70)
        if info and info.get("context"):
            print("[OK] Game Context")
        if info and info.get("gameplay"):
            print("[OK] Gameplay Description")
        if info and info.get("objectives"):
            obj_count = len(info["objectives"]) if isinstance(info["objectives"], list) else 1
            print(f"[OK] Learning Objectives ({obj_count} objectives)")
        if info and info.get("lang_analysis"):
            print("[OK] Language File Analysis (NPC dialogue & narrative)")
        if info and info.get("document_analysis"):
            doc_count = len(info["document_analysis"]) if isinstance(info["document_analysis"], dict) else 1
            print(f"[OK] Document Analysis ({doc_count} document(s))")
        if metadata and metadata.get("world_files"):
            print("[OK] World File Information")
        print("-" * 70)
        print("\n⏳ Processing...\n")
        
        result = self.game_manager.create_leadership_sheet(self.current_game)
        
        if result:
            print(f"\n[OK] Leadership information sheet created successfully!")
            print(f"\n Saved to: {result}")
            
            # Ask if user wants to view it
            view = input("\nView the sheet now? (y/n): ").strip().lower()
            if view == 'y':
                self.clear_screen()
                print("=" * 70)
                print("SCHOOL LEADERSHIP INFORMATION SHEET")
                print("=" * 70)
                try:
                    with open(result, 'r', encoding='utf-8') as f:
                        print(f.read())
                except Exception as e:
                    print(f"Error reading file: {e}")
        else:
            print("\n[ERROR] Failed to create leadership information sheet.")
        
        self.wait_for_key()
    
    def create_curriculum_mapping(self):
        """Create a curriculum standards mapping document."""
        if not self.settings.is_configured():
            print("\n[ERROR] Azure OpenAI must be configured to use creation features!")
            self.wait_for_key()
            return
        
        self.clear_screen()
        print("=" * 70)
        print(f"    CREATE CURRICULUM STANDARDS MAPPING - {self.current_game}")
        print("=" * 70)
        
        # Country selection
        print("\n Select Country/Region:")
        print("-" * 70)
        countries = [
            "United States",
            "United Kingdom",
            "Canada",
            "Australia",
            "New Zealand",
            "Singapore",
            "European Union",
            "International (IB)",
            "Other"
        ]
        
        for i, country in enumerate(countries, 1):
            print(f"{i}. {country}")
        
        try:
            country_choice = int(input("\nEnter country number (0 to cancel): ").strip())
            if country_choice == 0:
                return
            elif 1 <= country_choice <= len(countries):
                selected_country = countries[country_choice - 1]
            else:
                print("\n[ERROR] Invalid choice!")
                self.wait_for_key()
                return
        except ValueError:
            print("\n[ERROR] Invalid input!")
            self.wait_for_key()
            return
        
        # Handle "Other" country
        if selected_country == "Other":
            selected_country = input("\nEnter country/region name: ").strip()
            if not selected_country:
                print("\n[ERROR] Country name cannot be empty!")
                self.wait_for_key()
                return
        
        # Standards selection based on country
        print(f"\n Select Standards for {selected_country}:")
        print("-" * 70)
        
        # Define standards by country
        standards_options = {
            "United States": [
                "Common Core State Standards (CCSS)",
                "Next Generation Science Standards (NGSS)",
                "ISTE Standards for Students",
                "C3 Framework (Social Studies)",
                "National Core Arts Standards",
                "State-specific Standards"
            ],
            "United Kingdom": [
                "National Curriculum for England",
                "Scottish Curriculum for Excellence",
                "Welsh Curriculum",
                "Northern Ireland Curriculum",
                "Computing at School (CAS) Standards"
            ],
            "Canada": [
                "Provincial Curriculum Standards",
                "Common Curriculum Framework",
                "Digital Literacy Framework",
                "Indigenous Education Standards"
            ],
            "Australia": [
                "Australian Curriculum (ACARA)",
                "Digital Technologies Curriculum",
                "General Capabilities",
                "Cross-curriculum Priorities"
            ],
            "New Zealand": [
                "New Zealand Curriculum",
                "Te Marautanga o Aotearoa",
                "Digital Technologies & Hangarau Matihiko"
            ],
            "Singapore": [
                "MOE Curriculum Standards",
                "21st Century Competencies Framework",
                "Subject-based Banding Standards"
            ],
            "European Union": [
                "Key Competences for Lifelong Learning",
                "Digital Competence Framework (DigComp)",
                "National Education Standards"
            ],
            "International (IB)": [
                "IB Primary Years Programme (PYP)",
                "IB Middle Years Programme (MYP)",
                "IB Diploma Programme (DP)",
                "IB Career-related Programme (CP)"
            ]
        }
        
        # Get standards for selected country or use generic for "Other"
        available_standards = standards_options.get(selected_country, [
            "National Standards",
            "Subject-specific Standards",
            "Digital Literacy Standards",
            "21st Century Skills Framework"
        ])
        
        print("\nSelect all standards to map (enter numbers separated by commas):")
        for i, standard in enumerate(available_standards, 1):
            print(f"{i}. {standard}")
        print(f"{len(available_standards) + 1}. All of the above")
        
        standards_input = input("\nYour selection: ").strip()
        
        try:
            if not standards_input:
                print("\n[ERROR] No standards selected!")
                self.wait_for_key()
                return
            
            # Parse selection
            if standards_input == str(len(available_standards) + 1):
                selected_standards = available_standards
            else:
                indices = [int(x.strip()) for x in standards_input.split(',')]
                selected_standards = [available_standards[i-1] for i in indices if 1 <= i <= len(available_standards)]
            
            if not selected_standards:
                print("\n[ERROR] No valid standards selected!")
                self.wait_for_key()
                return
        
        except (ValueError, IndexError):
            print("\n[ERROR] Invalid input!")
            self.wait_for_key()
            return
        
        # Show summary and confirm
        self.clear_screen()
        print("=" * 70)
        print(f"    CURRICULUM STANDARDS MAPPING - {self.current_game}")
        print("=" * 70)
        
        print(f"\n Country/Region: {selected_country}")
        print("\n Selected Standards:")
        for standard in selected_standards:
            print(f"  [OK] {standard}")
        
        # Show what information is available
        print("\n Using the following game information:")
        print("-" * 70)
        info = self.game_manager.load_game_info(self.current_game)
        metadata = self.game_manager._load_metadata(self.current_game)
        
        if info and info.get("context"):
            print("[OK] Game Context")
        if info and info.get("gameplay"):
            print("[OK] Gameplay Description")
        if info and info.get("objectives"):
            obj_count = len(info["objectives"]) if isinstance(info["objectives"], list) else 1
            print(f"[OK] Learning Objectives ({obj_count} objectives)")
        if info and info.get("lang_analysis"):
            print("[OK] Language File Analysis (NPC dialogue & narrative)")
        if info and info.get("document_analysis"):
            doc_count = len(info["document_analysis"]) if isinstance(info["document_analysis"], dict) else 1
            print(f"[OK] Document Analysis ({doc_count} document(s))")
        if metadata and metadata.get("world_files"):
            print("[OK] World File Information")
        print("-" * 70)
        
        confirm = input("\n\nProceed with mapping? (y/n): ").strip().lower()
        if confirm != 'y':
            print("\n[ERROR] Cancelled.")
            self.wait_for_key()
            return
        
        print("\n⏳ Generating curriculum standards mapping...\n")
        
        result = self.game_manager.create_curriculum_mapping(
            self.current_game,
            selected_country,
            selected_standards
        )
        
        if result:
            print(f"\n[OK] Curriculum standards mapping created successfully!")
            print(f"\n Saved to: {result}")
            
            # Ask if user wants to view it
            view = input("\nView the mapping now? (y/n): ").strip().lower()
            if view == 'y':
                self.clear_screen()
                print("=" * 70)
                print("CURRICULUM STANDARDS MAPPING")
                print("=" * 70)
                try:
                    with open(result, 'r', encoding='utf-8') as f:
                        print(f.read())
                except Exception as e:
                    print(f"Error reading file: {e}")
        else:
            print("\n[ERROR] Failed to create curriculum standards mapping.")
        
        self.wait_for_key()
    
    def create_text_complexity_analysis(self):
        """Create a text complexity analysis with simplification recommendations."""
        if not self.settings.is_configured():
            print("\n[ERROR] Azure OpenAI must be configured to use creation features!")
            self.wait_for_key()
            return
        
        self.clear_screen()
        print("=" * 70)
        print(f"    CREATE TEXT COMPLEXITY ANALYSIS - {self.current_game}")
        print("=" * 70)
        
        # Check if language file analysis exists
        info = self.game_manager.load_game_info(self.current_game)
        metadata = self.game_manager._load_metadata(self.current_game)
        
        if not info or not info.get("lang_analysis"):
            print("\n[ERROR] No language file analysis found!")
            print("   Please upload a world file and extract language files first.")
            print("   Use option 3 to upload a world file, then option 7 to extract.")
            self.wait_for_key()
            return
        
        print("\n Generating text complexity analysis...\n")
        
        # Show what information is available
        print(" Using the following information:")
        print("-" * 70)
        print("[OK] Language File Analysis (NPC dialogue & in-game text)")
        if info and info.get("context"):
            print("[OK] Game Context")
        if info and info.get("objectives"):
            obj_count = len(info["objectives"]) if isinstance(info["objectives"], list) else 1
            print(f"[OK] Learning Objectives ({obj_count} objectives)")
        if metadata and metadata.get("lang_file"):
            print(f"[OK] Language File: {metadata['lang_file']['filename']}")
        print("-" * 70)
        print("\n⏳ Processing...\n")
        
        result = self.game_manager.create_text_complexity_analysis(self.current_game)
        
        if result:
            print(f"\n[OK] Text complexity analysis created successfully!")
            print(f"\n Saved to: {result}")
            
            # Ask if user wants to view it
            view = input("\nView the analysis now? (y/n): ").strip().lower()
            if view == 'y':
                self.clear_screen()
                print("=" * 70)
                print("TEXT COMPLEXITY ANALYSIS")
                print("=" * 70)
                try:
                    with open(result, 'r', encoding='utf-8') as f:
                        print(f.read())
                except Exception as e:
                    print(f"Error reading file: {e}")
        else:
            print("\n[ERROR] Failed to create text complexity analysis.")
        
        self.wait_for_key()
    
    def settings_menu(self):
        """Settings menu for Azure OpenAI API configuration."""
        while True:
            self.clear_screen()
            print("=" * 70)
            print("    SETTINGS - AZURE OPENAI API")
            print("=" * 70)
            
            config = self.settings.get_config()
            
            print("\nCurrent Configuration:")
            print("-" * 60)
            print(f"API Endpoint: {config.get('endpoint', 'Not set')}")
            print(f"API Key: {'*' * 20 if config.get('api_key') else 'Not set'}")
            print(f"Deployment: {config.get('deployment', 'Not set')}")
            print(f"API Version: {config.get('api_version', 'Not set')}")
            
            print("\n" + "-" * 60)
            print("1. Set API Endpoint")
            print("2. Set API Key")
            print("3. Set Deployment Name")
            print("4. Set API Version")
            print("5. Test Connection")
            print("6. Clear Configuration")
            print("0. Back to Main Menu")
            print("-" * 60)
            
            choice = input("\nEnter your choice: ").strip()
            
            if choice == "1":
                endpoint = input("\nEnter Azure OpenAI endpoint: ").strip()
                if endpoint:
                    self.settings.set_config("endpoint", endpoint)
                    print("[OK] Endpoint saved!")
                    self.wait_for_key()
            
            elif choice == "2":
                api_key = input("\nEnter Azure OpenAI API key: ").strip()
                if api_key:
                    self.settings.set_config("api_key", api_key)
                    print("[OK] API key saved!")
                    self.wait_for_key()
            
            elif choice == "3":
                deployment = input("\nEnter deployment name: ").strip()
                if deployment:
                    self.settings.set_config("deployment", deployment)
                    print("[OK] Deployment name saved!")
                    self.wait_for_key()
            
            elif choice == "4":
                api_version = input("\nEnter API version (e.g., 2024-02-15-preview): ").strip()
                if api_version:
                    self.settings.set_config("api_version", api_version)
                    print("[OK] API version saved!")
                    self.wait_for_key()
            
            elif choice == "5":
                if self.settings.is_configured():
                    print("\n Testing connection...")
                    if self.game_manager.test_azure_connection():
                        print("[OK] Connection successful!")
                    else:
                        print("[ERROR] Connection failed!")
                else:
                    print("\n[ERROR] Please configure all settings first!")
                self.wait_for_key()
            
            elif choice == "6":
                confirm = input("\nAre you sure you want to clear all settings? (yes/no): ").strip().lower()
                if confirm == "yes":
                    self.settings.clear_config()
                    print("[OK] Configuration cleared!")
                    self.wait_for_key()
            
            elif choice == "0":
                break
    
    def run(self):
        """Main application loop."""
        while True:
            self.display_main_menu()
            choice = input("\nEnter your choice: ").strip().lower()
            
            if choice == "1":
                self.create_new_game()
            elif choice == "2":
                self.load_existing_game()
            elif choice == "3":
                if self.current_game:
                    self.upload_world_file()
                else:
                    print("\n[ERROR] Please load a game first!")
                    self.wait_for_key()
            elif choice == "4":
                if self.current_game:
                    self.add_game_context()
                else:
                    print("\n[ERROR] Please load a game first!")
                    self.wait_for_key()
            elif choice == "5":
                if self.current_game:
                    self.add_gameplay_description()
                else:
                    print("\n[ERROR] Please load a game first!")
                    self.wait_for_key()
            elif choice == "6":
                if self.current_game:
                    self.add_learning_objectives()
                else:
                    print("\n[ERROR] Please load a game first!")
                    self.wait_for_key()
            elif choice == "7":
                if self.current_game:
                    self.extract_lang_files()
                else:
                    print("\n[ERROR] Please load a game first!")
                    self.wait_for_key()
            elif choice == "e":
                if self.current_game:
                    self.export_all_creations()
                else:
                    print("\n[ERROR] Please load a game first!")
                    self.wait_for_key()
            elif choice == "d" or choice == "doc" or choice == "docs":
                if self.current_game:
                    self.upload_analyze_documents()
                else:
                    print("\n[ERROR] Please load a game first!")
                    self.wait_for_key()
            elif choice == "r" or choice == "remove":
                if self.current_game:
                    self.remove_documents()
                else:
                    print("\n[ERROR] Please load a game first!")
                    self.wait_for_key()
            elif choice == "a":
                if self.current_game:
                    self.create_student_guide()
                else:
                    print("\n[ERROR] Please load a game first!")
                    self.wait_for_key()
            elif choice == "b":
                if self.current_game:
                    self.create_student_workbook()
                else:
                    print("\n[ERROR] Please load a game first!")
                    self.wait_for_key()
            elif choice == "c":
                if self.current_game:
                    self.create_student_quiz()
                else:
                    print("\n[ERROR] Please load a game first!")
                    self.wait_for_key()
            elif choice == "p" or choice == "parent":
                if self.current_game:
                    self.create_parent_guide()
                else:
                    print("\n[ERROR] Please load a game first!")
                    self.wait_for_key()
            elif choice == "t" or choice == "teacher":
                if self.current_game:
                    self.create_teacher_guide()
                else:
                    print("\n[ERROR] Please load a game first!")
                    self.wait_for_key()
            elif choice == "sl" or choice == "leadership":
                if self.current_game:
                    self.create_leadership_sheet()
                else:
                    print("\n[ERROR] Please load a game first!")
                    self.wait_for_key()
            elif choice == "cs" or choice == "curriculum" or choice == "standards":
                if self.current_game:
                    self.create_curriculum_mapping()
                else:
                    print("\n[ERROR] Please load a game first!")
                    self.wait_for_key()
            elif choice == "tc" or choice == "text" or choice == "complexity":
                if self.current_game:
                    self.create_text_complexity_analysis()
                else:
                    print("\n[ERROR] Please load a game first!")
                    self.wait_for_key()
            elif choice == "s" or choice == "settings":
                self.settings_menu()
            elif choice == "l" or choice == "list":
                self.list_all_games()
            elif choice == "x" or choice == "delete":
                self.delete_game()
            elif choice == "0" or choice == "exit" or choice == "quit":
                self.clear_screen()
                print("\nThank you for using Minecraft Education Content Tools!")
                print("Goodbye! 👋\n")
                sys.exit(0)
            else:
                print("\n[ERROR] Invalid choice! Please try again.")
                self.wait_for_key()


if __name__ == "__main__":
    main()
