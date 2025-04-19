import pygame
import sys
import time
import math
import os

import tictactoe as ttt

pygame.init()
pygame.display.set_caption("Tic Tac Toe")

# Window size
size = width, height = 700, 500

# Define a function to track game state for stats
def update_stats_for_game():
    pass

# Load settings
settings = ttt.load_settings()
current_theme = settings.get("theme", ttt.THEME_CLASSIC)
current_pieces = settings.get("pieces", ttt.PIECES_CLASSIC)
custom_x_icon_path = settings.get("custom_x_icon", ttt.DEFAULT_X_ICON)
custom_o_icon_path = settings.get("custom_o_icon", ttt.DEFAULT_O_ICON)

# Cargar o crear íconos personalizados
custom_x_icon = None
custom_o_icon = None

def load_custom_icons():
    global custom_x_icon, custom_o_icon
    
    # Verificar si los archivos de íconos existen
    x_exists = os.path.exists(custom_x_icon_path)
    o_exists = os.path.exists(custom_o_icon_path)
    
    # Intentar cargar los íconos si existen
    if x_exists:
        try:
            custom_x_icon = pygame.image.load(custom_x_icon_path)
            # Asegurar que el tamaño sea adecuado (80x80)
            custom_x_icon = pygame.transform.scale(custom_x_icon, (80, 80))
        except pygame.error:
            print(f"No se pudo cargar el ícono X: {custom_x_icon_path}")
            custom_x_icon = None
    
    if o_exists:
        try:
            custom_o_icon = pygame.image.load(custom_o_icon_path)
            # Asegurar que el tamaño sea adecuado (80x80)
            custom_o_icon = pygame.transform.scale(custom_o_icon, (80, 80))
        except pygame.error:
            print(f"No se pudo cargar el ícono O: {custom_o_icon_path}")
            custom_o_icon = None

# Cargar los íconos al inicio
load_custom_icons()

# Colors - will be updated based on theme
black = (0, 0, 0)
white = (255, 255, 255)
gray = (200, 200, 200)
green = (50, 205, 50)
red = (220, 20, 60)
blue = (30, 144, 255)
purple = (128, 0, 128)
gold = (255, 215, 0)

# Apply theme colors
theme_colors = ttt.get_theme_colors(current_theme)
board_color = theme_colors["board_color"]
background_color = theme_colors["background_color"]
x_color = theme_colors["x_color"]
o_color = theme_colors["o_color"]
highlight_color = theme_colors["highlight_color"]

# Set up the display
screen = pygame.display.set_mode(size)

# Load fonts
smallFont = pygame.font.Font("OpenSans-Regular.ttf", 18)
mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)

# Game state variables
user = None
board = ttt.initial_state()
ai_turn = False
difficulty = None
showing_stats = False
showing_settings = False

# Load initial stats
stats = ttt.load_stats()

# Create icons for the settings screen
def draw_icon_button(screen, icon, position, size, selected=False, color=white):
    """Draw a button with an icon or symbol on it."""
    rect = pygame.Rect(position[0], position[1], size, size)
    
    # Draw button background
    if selected:
        pygame.draw.rect(screen, highlight_color, rect)
        pygame.draw.rect(screen, color, rect, 3)
    else:
        pygame.draw.rect(screen, gray, rect)
        pygame.draw.rect(screen, color, rect, 2)
    
    # Draw icon
    icon_text = moveFont.render(icon, True, color)
    icon_rect = icon_text.get_rect()
    icon_rect.center = rect.center
    screen.blit(icon_text, icon_rect)
    
    return rect

# Function to draw a bar chart for statistics
def draw_bar_chart(screen, stats, position, size, title):
    """Draw a simple bar chart showing game statistics."""
    chart_x, chart_y = position
    chart_width, chart_height = size
    
    # Draw title
    title_text = mediumFont.render(title, True, white)
    title_rect = title_text.get_rect()
    title_rect.center = (chart_x + chart_width // 2, chart_y - 10)
    screen.blit(title_text, title_rect)
    
    # Calculate values for display
    total = stats["player_wins"] + stats["ai_wins"] + stats["ties"]
    if total == 0:
        return
    
    bar_width = chart_width // 3 - 20
    max_bar_height = chart_height - 60
    
    # Draw player wins bar
    player_height = int((stats["player_wins"] / total) * max_bar_height)
    player_bar = pygame.Rect(chart_x, chart_y + max_bar_height - player_height, 
                             bar_width, player_height)
    pygame.draw.rect(screen, green, player_bar)
    
    # Draw AI wins bar
    ai_height = int((stats["ai_wins"] / total) * max_bar_height)
    ai_bar = pygame.Rect(chart_x + bar_width + 10, chart_y + max_bar_height - ai_height, 
                         bar_width, ai_height)
    pygame.draw.rect(screen, red, ai_bar)
    
    # Draw ties bar
    tie_height = int((stats["ties"] / total) * max_bar_height)
    tie_bar = pygame.Rect(chart_x + 2 * (bar_width + 10), chart_y + max_bar_height - tie_height, 
                          bar_width, tie_height)
    pygame.draw.rect(screen, blue, tie_bar)
    
    # Draw labels
    player_label = smallFont.render(f"Player: {stats['player_wins']}", True, green)
    player_rect = player_label.get_rect()
    player_rect.center = (chart_x + bar_width // 2, chart_y + max_bar_height + 15)
    screen.blit(player_label, player_rect)
    
    ai_label = smallFont.render(f"AI: {stats['ai_wins']}", True, red)
    ai_rect = ai_label.get_rect()
    ai_rect.center = (chart_x + bar_width + 10 + bar_width // 2, chart_y + max_bar_height + 15)
    screen.blit(ai_label, ai_rect)
    
    tie_label = smallFont.render(f"Ties: {stats['ties']}", True, blue)
    tie_rect = tie_label.get_rect()
    tie_rect.center = (chart_x + 2 * (bar_width + 10) + bar_width // 2, chart_y + max_bar_height + 15)
    screen.blit(tie_label, tie_rect)

# Function to draw a pie chart
def draw_pie_chart(screen, stats, position, radius, title):
    """Draw a pie chart showing game statistics."""
    pie_x, pie_y = position
    
    # Draw title
    title_text = mediumFont.render(title, True, white)
    title_rect = title_text.get_rect()
    title_rect.center = (pie_x, pie_y - radius - 20)
    screen.blit(title_text, title_rect)
    
    # Calculate values for display
    total = stats["games_played"]
    if total == 0:
        # Draw empty circle if no games played
        pygame.draw.circle(screen, gray, (pie_x, pie_y), radius, 2)
        return
    
    player_wins = stats["player_wins"]
    ai_wins = stats["ai_wins"]
    ties = stats["ties"]
    
    player_angle = player_wins / total * 360
    ai_angle = ai_wins / total * 360
    tie_angle = ties / total * 360
    
    # Draw the pie sections
    start_angle = 0
    
    # Player wins section (green)
    if player_wins > 0:
        end_angle = start_angle + player_angle
        for i in range(start_angle, int(end_angle), 1):
            pygame.draw.line(screen, green, (pie_x, pie_y), 
                            (pie_x + radius * math.sin(math.radians(i)), 
                             pie_y - radius * math.cos(math.radians(i))), 2)
        start_angle = end_angle
    
    # AI wins section (red)
    if ai_wins > 0:
        end_angle = start_angle + ai_angle
        for i in range(int(start_angle), int(end_angle), 1):
            pygame.draw.line(screen, red, (pie_x, pie_y), 
                            (pie_x + radius * math.sin(math.radians(i)), 
                             pie_y - radius * math.cos(math.radians(i))), 2)
        start_angle = end_angle
    
    # Ties section (blue)
    if ties > 0:
        end_angle = start_angle + tie_angle
        for i in range(int(start_angle), int(end_angle), 1):
            pygame.draw.line(screen, blue, (pie_x, pie_y), 
                            (pie_x + radius * math.sin(math.radians(i)), 
                             pie_y - radius * math.cos(math.radians(i))), 2)
    
    # Draw circle outline
    pygame.draw.circle(screen, white, (pie_x, pie_y), radius, 1)
    
    # Draw legend
    legend_x = pie_x - radius
    legend_y = pie_y + radius + 20
    
    # Player legend
    if player_wins > 0:
        pygame.draw.rect(screen, green, (legend_x, legend_y, 15, 15))
        player_text = smallFont.render(f"Player: {player_wins} ({int(player_wins/total*100)}%)", True, white)
        screen.blit(player_text, (legend_x + 25, legend_y))
        legend_y += 25
    
    # AI legend
    if ai_wins > 0:
        pygame.draw.rect(screen, red, (legend_x, legend_y, 15, 15))
        ai_text = smallFont.render(f"AI: {ai_wins} ({int(ai_wins/total*100)}%)", True, white)
        screen.blit(ai_text, (legend_x + 25, legend_y))
        legend_y += 25
    
    # Ties legend
    if ties > 0:
        pygame.draw.rect(screen, blue, (legend_x, legend_y, 15, 15))
        tie_text = smallFont.render(f"Ties: {ties} ({int(ties/total*100)}%)", True, white)
        screen.blit(tie_text, (legend_x + 25, legend_y))

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Set the background color based on theme
    screen.fill(background_color)

    # Settings screen
    if showing_settings:
        # Title
        title = largeFont.render("Customize Game", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)
        
        # Theme selection
        theme_title = mediumFont.render("Board Theme:", True, white)
        theme_rect = theme_title.get_rect()
        theme_rect.center = ((width / 2), 100)
        screen.blit(theme_title, theme_rect)
        
        # Theme buttons
        theme_buttons = {}
        theme_names = [ttt.THEME_CLASSIC, ttt.THEME_DARK, ttt.THEME_NEON, ttt.THEME_RETRO]
        theme_displays = ["Classic", "Dark", "Neon", "Retro"]
        
        for i, (theme, display) in enumerate(zip(theme_names, theme_displays)):
            btn_x = width // 5 + (i * 150)
            btn_y = 140
            btn_width = 100
            btn_height = 40
            
            btn_rect = pygame.Rect(btn_x, btn_y, btn_width, btn_height)
            
            # Highlight selected theme
            if theme == current_theme:
                pygame.draw.rect(screen, highlight_color, btn_rect)
            else:
                pygame.draw.rect(screen, gray, btn_rect)
                
            theme_text = smallFont.render(display, True, black)
            text_rect = theme_text.get_rect()
            text_rect.center = btn_rect.center
            screen.blit(theme_text, text_rect)
            
            theme_buttons[theme] = btn_rect
        
        # Piece style selection
        piece_title = mediumFont.render("Piece Style:", True, white)
        piece_rect = piece_title.get_rect()
        piece_rect.center = ((width / 2), 220)
        screen.blit(piece_title, piece_rect)
        
        # Piece style buttons 
        piece_icons = [
            (ttt.PIECES_CLASSIC, "X", "O"), 
            (ttt.PIECES_CUSTOM, "IMG", "IMG")
        ]
        
        piece_buttons = {}
        icon_size = 60
        
        for i, (piece_style, x_icon, o_icon) in enumerate(piece_icons):
            btn_x = width // 5 + (i * 150)
            btn_y = 260
            
            # Para los iconos personalizados, mostrar los íconos cargados si existen
            if piece_style == ttt.PIECES_CUSTOM:
                # Rectángulo para X
                x_rect = pygame.Rect(btn_x, btn_y, icon_size, icon_size)
                if current_pieces == ttt.PIECES_CUSTOM:
                    pygame.draw.rect(screen, highlight_color, x_rect)
                else:
                    pygame.draw.rect(screen, gray, x_rect)
                pygame.draw.rect(screen, white, x_rect, 2)
                
                # Mostrar ícono X si existe
                if custom_x_icon is not None:
                    # Escalar para que quepa en el botón
                    scaled_icon = pygame.transform.scale(custom_x_icon, (icon_size-10, icon_size-10))
                    icon_rect = scaled_icon.get_rect()
                    icon_rect.center = x_rect.center
                    screen.blit(scaled_icon, icon_rect)
                else:
                    # Mostrar texto si no hay ícono
                    icon_text = smallFont.render("X Icon", True, white)
                    icon_rect = icon_text.get_rect()
                    icon_rect.center = x_rect.center
                    screen.blit(icon_text, icon_rect)
                
                # Rectángulo para O
                o_rect = pygame.Rect(btn_x + icon_size + 10, btn_y, icon_size, icon_size)
                if current_pieces == ttt.PIECES_CUSTOM:
                    pygame.draw.rect(screen, highlight_color, o_rect)
                else:
                    pygame.draw.rect(screen, gray, o_rect)
                pygame.draw.rect(screen, white, o_rect, 2)
                
                # Mostrar ícono O si existe
                if custom_o_icon is not None:
                    # Escalar para que quepa en el botón
                    scaled_icon = pygame.transform.scale(custom_o_icon, (icon_size-10, icon_size-10))
                    icon_rect = scaled_icon.get_rect()
                    icon_rect.center = o_rect.center
                    screen.blit(scaled_icon, icon_rect)
                else:
                    # Mostrar texto si no hay ícono
                    icon_text = smallFont.render("O Icon", True, white)
                    icon_rect = icon_text.get_rect()
                    icon_rect.center = o_rect.center
                    screen.blit(icon_text, icon_rect)
            else:
                # Para los demás estilos, mostrar los íconos de texto
                x_rect = draw_icon_button(screen, x_icon, (btn_x, btn_y), icon_size, 
                                        selected=(piece_style == current_pieces))
                
                o_rect = draw_icon_button(screen, o_icon, (btn_x + icon_size + 10, btn_y), icon_size,
                                        selected=(piece_style == current_pieces))
            
            # Store the combined area of both icons for click detection
            piece_buttons[piece_style] = pygame.Rect(btn_x, btn_y, icon_size*2 + 10, icon_size)
            
        # Instrucciones para íconos personalizados
        if current_pieces == ttt.PIECES_CUSTOM:
            custom_instructions = smallFont.render("Para usar tus propios íconos, colócalos en /assets/icons/ como x_icon.png y o_icon.png", True, white)
            instructions_rect = custom_instructions.get_rect()
            instructions_rect.center = ((width / 2), 340)
            screen.blit(custom_instructions, instructions_rect)
            
            # Botón para recargar íconos
            reload_btn = pygame.Rect((width / 2) - 60, 360, 120, 30)
            pygame.draw.rect(screen, blue, reload_btn)
            reload_text = smallFont.render("Recargar íconos", True, black)
            reload_rect = reload_text.get_rect()
            reload_rect.center = reload_btn.center
            screen.blit(reload_text, reload_rect)
        
        # Save and back buttons
        saveButton = pygame.Rect(width // 4, height - 80, width // 4, 50)
        backButton = pygame.Rect(width // 2, height - 80, width // 4, 50)
        
        pygame.draw.rect(screen, green, saveButton)
        save_text = mediumFont.render("Save", True, black)
        save_rect = save_text.get_rect()
        save_rect.center = saveButton.center
        screen.blit(save_text, save_rect)
        
        pygame.draw.rect(screen, red, backButton)
        back_text = mediumFont.render("Cancel", True, black)
        back_rect = back_text.get_rect()
        back_rect.center = backButton.center
        screen.blit(back_text, back_rect)
        
        # Handle button clicks
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            
            # Theme buttons
            for theme, btn_rect in theme_buttons.items():
                if btn_rect.collidepoint(mouse):
                    time.sleep(0.2)
                    current_theme = theme
                    # Apply theme colors
                    theme_colors = ttt.get_theme_colors(current_theme)
                    board_color = theme_colors["board_color"]
                    background_color = theme_colors["background_color"]
                    x_color = theme_colors["x_color"]
                    o_color = theme_colors["o_color"]
                    highlight_color = theme_colors["highlight_color"]
            
            # Piece style buttons
            for piece_style, btn_rect in piece_buttons.items():
                if btn_rect.collidepoint(mouse):
                    time.sleep(0.2)
                    current_pieces = piece_style
            
            # Botón para recargar íconos personalizados
            if current_pieces == ttt.PIECES_CUSTOM and 'reload_btn' in locals() and reload_btn.collidepoint(mouse):
                time.sleep(0.2)
                load_custom_icons()
            
            # Save button
            if saveButton.collidepoint(mouse):
                time.sleep(0.2)
                settings = {
                    "theme": current_theme,
                    "pieces": current_pieces,
                    "board_color": board_color,
                    "background_color": background_color,
                    "x_color": x_color,
                    "o_color": o_color,
                    "custom_x_icon": custom_x_icon_path,
                    "custom_o_icon": custom_o_icon_path
                }
                ttt.save_settings(settings)
                showing_settings = False
            
            # Back button
            if backButton.collidepoint(mouse):
                time.sleep(0.2)
                # Revert to previously saved settings
                settings = ttt.load_settings()
                current_theme = settings.get("theme", ttt.THEME_CLASSIC)
                current_pieces = settings.get("pieces", ttt.PIECES_CLASSIC)
                custom_x_icon_path = settings.get("custom_x_icon", ttt.DEFAULT_X_ICON)
                custom_o_icon_path = settings.get("custom_o_icon", ttt.DEFAULT_O_ICON)
                
                # Apply theme colors
                theme_colors = ttt.get_theme_colors(current_theme)
                board_color = theme_colors["board_color"]
                background_color = theme_colors["background_color"]
                x_color = theme_colors["x_color"]
                o_color = theme_colors["o_color"]
                highlight_color = theme_colors["highlight_color"]
                
                showing_settings = False

    # Statistics screen
    elif showing_stats:
        # Title
        title = largeFont.render("Game Statistics", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)
        
        # Draw pie chart
        draw_pie_chart(screen, stats, (width // 4, height // 2 - 30), 80, "Overall Results")
        
        # Draw bar chart for difficulty stats
        chart_x = width // 2 + 70
        chart_y = 150
        chart_width = 250
        chart_height = 220
        
        # Draw overall stats text above the charts
        games_text = mediumFont.render(f"Total Games: {stats['games_played']}", True, gold)
        games_rect = games_text.get_rect()
        games_rect.center = ((width / 2), 100)
        screen.blit(games_text, games_rect)
        
        # Draw difficulty stats
        diff_title = mediumFont.render("By Difficulty", True, white)
        diff_rect = diff_title.get_rect()
        diff_rect.center = (chart_x + chart_width // 2, chart_y - 10)
        screen.blit(diff_title, diff_rect)
        
        # Display difficulty stats for each level
        y_pos = chart_y + 20
        for diff in [ttt.EASY, ttt.MEDIUM, ttt.HARD]:
            diff_stats = stats["by_difficulty"][diff]
            diff_games = diff_stats["games"]
            
            diff_color = green if diff == ttt.EASY else (blue if diff == ttt.MEDIUM else red)
            diff_text = smallFont.render(f"{diff.capitalize()}: {diff_games} games", True, diff_color)
            diff_rect = diff_text.get_rect()
            diff_rect.topleft = (chart_x, y_pos)
            screen.blit(diff_text, diff_rect)
            
            # Only show percentages if games have been played at this difficulty
            if diff_games > 0:
                player_win_pct = int(diff_stats["player_wins"] / diff_games * 100)
                ai_win_pct = int(diff_stats["ai_wins"] / diff_games * 100)
                tie_pct = int(diff_stats["ties"] / diff_games * 100)
                
                # Draw mini progress bars for each stat
                bar_width = 200
                bar_height = 15
                
                # Background bar
                pygame.draw.rect(screen, gray, (chart_x, y_pos + 25, bar_width, bar_height))
                
                # Player wins (green)
                if player_win_pct > 0:
                    pygame.draw.rect(screen, green, 
                                    (chart_x, y_pos + 25, 
                                     bar_width * player_win_pct // 100, bar_height))
                
                # AI wins (red)
                if ai_win_pct > 0:
                    pygame.draw.rect(screen, red, 
                                    (chart_x + bar_width * player_win_pct // 100, y_pos + 25, 
                                     bar_width * ai_win_pct // 100, bar_height))
                
                # Ties (blue)
                if tie_pct > 0:
                    pygame.draw.rect(screen, blue, 
                                    (chart_x + bar_width * (player_win_pct + ai_win_pct) // 100, y_pos + 25, 
                                     bar_width * tie_pct // 100, bar_height))
                
                # Labels for percentages
                stats_text = smallFont.render(
                    f"Player: {player_win_pct}% | AI: {ai_win_pct}% | Ties: {tie_pct}%", 
                    True, 
                    white
                )
                stats_rect = stats_text.get_rect()
                stats_rect.topleft = (chart_x, y_pos + 45)
                screen.blit(stats_text, stats_rect)
            
            y_pos += 70
        
        # Back button
        backButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
        back = mediumFont.render("Back", True, black)
        backRect = back.get_rect()
        backRect.center = backButton.center
        pygame.draw.rect(screen, white, backButton)
        screen.blit(back, backRect)
        
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if backButton.collidepoint(mouse):
                time.sleep(0.2)
                showing_stats = False
    
    # Main menu screen
    elif user is None:
        # Draw title
        title = largeFont.render("Tic Tac Toe", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Draw buttons for X or O
        playXButton = pygame.Rect((width / 8), (height / 2) - 70, width / 4, 50)
        playX = mediumFont.render(f"Play as {ttt.get_piece_symbol(ttt.X, current_pieces)}", True, black)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, x_color, playXButton)
        screen.blit(playX, playXRect)

        playOButton = pygame.Rect(5 * (width / 8), (height / 2) - 70, width / 4, 50)
        playO = mediumFont.render(f"Play as {ttt.get_piece_symbol(ttt.O, current_pieces)}", True, black)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, o_color, playOButton)
        screen.blit(playO, playORect)
        
        # Draw difficulty selection buttons
        difficultyText = mediumFont.render("Select Difficulty:", True, white)
        difficultyRect = difficultyText.get_rect()
        difficultyRect.center = ((width / 2), (height / 2) + 10)
        screen.blit(difficultyText, difficultyRect)
        
        diff_y = (height / 2) + 50
        easyButton = pygame.Rect((width / 8), diff_y, width / 5, 50)
        easy = mediumFont.render("Easy", True, black)
        easyRect = easy.get_rect()
        easyRect.center = easyButton.center
        pygame.draw.rect(screen, green, easyButton)
        screen.blit(easy, easyRect)
        
        mediumButton = pygame.Rect((width / 2) - (width / 10), diff_y, width / 5, 50)
        medium = mediumFont.render("Medium", True, black)
        mediumRect = medium.get_rect()
        mediumRect.center = mediumButton.center
        pygame.draw.rect(screen, blue, mediumButton)
        screen.blit(medium, mediumRect)
        
        hardButton = pygame.Rect(7 * (width / 10) - (width / 20), diff_y, width / 5, 50)
        hard = mediumFont.render("Hard", True, black)
        hardRect = hard.get_rect()
        hardRect.center = hardButton.center
        pygame.draw.rect(screen, red, hardButton)
        screen.blit(hard, hardRect)
        
        # Bottom buttons row
        button_y = (height / 2) + 120
        button_width = width / 4
        button_spacing = (width - 3 * button_width) / 4
        
        # Add Statistics button
        statsButton = pygame.Rect(button_spacing, button_y, button_width, 50)
        statsText = mediumFont.render("Statistics", True, black)
        statsRect = statsText.get_rect()
        statsRect.center = statsButton.center
        pygame.draw.rect(screen, white, statsButton)
        screen.blit(statsText, statsRect)
        
        # Add Settings button
        settingsButton = pygame.Rect(2 * button_spacing + button_width, button_y, button_width, 50)
        settingsText = mediumFont.render("Customize", True, black)
        settingsRect = settingsText.get_rect()
        settingsRect.center = settingsButton.center
        pygame.draw.rect(screen, purple, settingsButton)
        screen.blit(settingsText, settingsRect)
        
        # Add Quit button
        quitButton = pygame.Rect(3 * button_spacing + 2 * button_width, button_y, button_width, 50)
        quitText = mediumFont.render("Quit", True, black)
        quitRect = quitText.get_rect()
        quitRect.center = quitButton.center
        pygame.draw.rect(screen, gray, quitButton)
        screen.blit(quitText, quitRect)
        
        # Display current selections
        if user is not None:
            userText = mediumFont.render(f"Player: {ttt.get_piece_symbol(user, current_pieces)}", True, white)
            userRect = userText.get_rect()
            userRect.center = ((width / 2), (height / 2) + 190)
            screen.blit(userText, userRect)
            
        if difficulty is not None:
            diffColor = green if difficulty == ttt.EASY else (blue if difficulty == ttt.MEDIUM else red)
            diffText = mediumFont.render(f"Difficulty: {difficulty.capitalize()}", True, diffColor)
            diffRect = diffText.get_rect()
            diffRect.center = ((width / 2), (height / 2) + 220)
            screen.blit(diffText, diffRect)

        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.X
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.O
            elif easyButton.collidepoint(mouse):
                time.sleep(0.2)
                difficulty = ttt.EASY
            elif mediumButton.collidepoint(mouse):
                time.sleep(0.2)
                difficulty = ttt.MEDIUM
            elif hardButton.collidepoint(mouse):
                time.sleep(0.2)
                difficulty = ttt.HARD
            elif statsButton.collidepoint(mouse):
                time.sleep(0.2)
                # Refresh stats before showing them
                stats = ttt.load_stats()
                showing_stats = True
            elif settingsButton.collidepoint(mouse):
                time.sleep(0.2)
                showing_settings = True
            elif quitButton.collidepoint(mouse):
                time.sleep(0.2)
                pygame.quit()
                sys.exit()
                
        # Start game once player and difficulty are selected
        if user is not None and difficulty is not None:
            time.sleep(0.5)  # Short delay before starting game
            # If user is O, AI goes first
            if user == ttt.O:
                ai_turn = True

    # Game screen
    else:
        # Draw game board
        tile_size = 100
        tile_origin = (width / 2 - (1.5 * tile_size),
                       height / 2 - (1.5 * tile_size))
        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                pygame.draw.rect(screen, board_color, rect, 3)

                if board[i][j] != ttt.EMPTY:
                    # Si estamos usando íconos personalizados
                    if current_pieces == ttt.PIECES_CUSTOM:
                        # Si el ícono está cargado, mostrarlo
                        if board[i][j] == ttt.X and custom_x_icon is not None:
                            # Centrar el ícono en la celda
                            icon_rect = custom_x_icon.get_rect()
                            icon_rect.center = rect.center
                            screen.blit(custom_x_icon, icon_rect)
                        elif board[i][j] == ttt.O and custom_o_icon is not None:
                            # Centrar el ícono en la celda
                            icon_rect = custom_o_icon.get_rect()
                            icon_rect.center = rect.center
                            screen.blit(custom_o_icon, icon_rect)
                        else:
                            # Fallback a texto si no hay ícono
                            piece_color = x_color if board[i][j] == ttt.X else o_color
                            piece_symbol = ttt.get_piece_symbol(board[i][j], ttt.PIECES_CLASSIC)
                            move = moveFont.render(piece_symbol, True, piece_color)
                            moveRect = move.get_rect()
                            moveRect.center = rect.center
                            screen.blit(move, moveRect)
                    else:
                        # Usar el estilo de pieza seleccionado (texto)
                        piece_color = x_color if board[i][j] == ttt.X else o_color
                        piece_symbol = ttt.get_piece_symbol(board[i][j], current_pieces)
                        move = moveFont.render(piece_symbol, True, piece_color)
                        moveRect = move.get_rect()
                        moveRect.center = rect.center
                        screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        game_over = ttt.terminal(board)
        player_current = ttt.player(board)
        
        # If game just ended, update stats
        if game_over and not showing_stats:
            game_winner = ttt.winner(board)
            # Use a variable to track if we've already processed this game
            if not hasattr(update_stats_for_game, "last_game_processed") or update_stats_for_game.last_game_processed != board:
                ttt.update_stats(user, game_winner, difficulty)
                # Reload stats to get the updated values
                stats = ttt.load_stats()
                update_stats_for_game.last_game_processed = board

        # Show title
        if game_over:
            winner = ttt.winner(board)
            if winner is None:
                title = f"Game Over: Tie."
            else:
                winner_symbol = ttt.get_piece_symbol(winner, current_pieces)
                title = f"Game Over: {winner_symbol} wins!"
        elif user == player_current:
            player_symbol = ttt.get_piece_symbol(user, current_pieces)
            title = f"Your Turn ({player_symbol})"
        else:
            title = f"Computer Thinking..."
        title = largeFont.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)
        
        # Display current difficulty with appropriate color
        if difficulty is not None:
            diffColor = green if difficulty == ttt.EASY else (blue if difficulty == ttt.MEDIUM else red)
            diffText = mediumFont.render(f"Difficulty: {difficulty.capitalize()}", True, diffColor)
            diffRect = diffText.get_rect()
            diffRect.center = ((width / 2), 70)
            screen.blit(diffText, diffRect)
        else:
            # Set a default difficulty if it somehow became None
            difficulty = ttt.MEDIUM
            diffText = mediumFont.render(f"Difficulty: {difficulty.capitalize()}", True, blue)
            diffRect = diffText.get_rect()
            diffRect.center = ((width / 2), 70)
            screen.blit(diffText, diffRect)

        # Check for AI move
        if user != player_current and not game_over:
            if ai_turn:
                time.sleep(0.5)
                move = ttt.minimax(board, difficulty)
                board = ttt.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        # Check for a user move
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player_current and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if (board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse)):
                        board = ttt.result(board, (i, j))

        if game_over:
            # Show buttons for play again, stats, customize, and main menu
            button_width = width / 5
            button_spacing = (width - 4 * button_width) / 5
            button_y = height - 65
            
            # Play Again button
            againButton = pygame.Rect(button_spacing, button_y, button_width, 50)
            again = smallFont.render("Play Again", True, black)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, green, againButton)
            screen.blit(again, againRect)
            
            # Statistics button
            statsButton = pygame.Rect(2 * button_spacing + button_width, button_y, button_width, 50)
            statsText = smallFont.render("Statistics", True, black)
            statsRect = statsText.get_rect()
            statsRect.center = statsButton.center
            pygame.draw.rect(screen, blue, statsButton)
            screen.blit(statsText, statsRect)
            
            # Customize button
            customizeButton = pygame.Rect(3 * button_spacing + 2 * button_width, button_y, button_width, 50)
            customizeText = smallFont.render("Customize", True, black)
            customizeRect = customizeText.get_rect()
            customizeRect.center = customizeButton.center
            pygame.draw.rect(screen, purple, customizeButton)
            screen.blit(customizeText, customizeRect)
            
            # Main Menu button
            menuButton = pygame.Rect(4 * button_spacing + 3 * button_width, button_y, button_width, 50)
            menuText = smallFont.render("Main Menu", True, black)
            menuRect = menuText.get_rect()
            menuRect.center = menuButton.center
            pygame.draw.rect(screen, gray, menuButton)
            screen.blit(menuText, menuRect)
            
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    board = ttt.initial_state()
                    ai_turn = (user == ttt.O)  # If user is O, AI goes first
                elif statsButton.collidepoint(mouse):
                    time.sleep(0.2)
                    showing_stats = True
                    # Reload stats before showing
                    stats = ttt.load_stats()
                elif customizeButton.collidepoint(mouse):
                    time.sleep(0.2)
                    showing_settings = True
                elif menuButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = ttt.initial_state()
                    ai_turn = False
                    difficulty = None

    pygame.display.flip()
