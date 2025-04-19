import pygame
import sys
import time

import tictactoe as ttt

pygame.init()
size = width, height = 600, 400

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
gray = (200, 200, 200)
green = (50, 205, 50)
red = (220, 20, 60)
blue = (30, 144, 255)

# Define a function to track game state for stats
def update_stats_for_game():
    pass

screen = pygame.display.set_mode(size)

smallFont = pygame.font.Font("OpenSans-Regular.ttf", 18)
mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)

user = None
board = ttt.initial_state()
ai_turn = False
difficulty = None
showing_stats = False

# Load initial stats
stats = ttt.load_stats()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(black)

    # Show statistics screen
    if showing_stats:
        # Title
        title = largeFont.render("Game Statistics", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)
        
        # Overall stats
        overall_text = mediumFont.render("Overall Statistics", True, blue)
        overall_rect = overall_text.get_rect()
        overall_rect.center = ((width / 2), 100)
        screen.blit(overall_text, overall_rect)
        
        games_text = smallFont.render(f"Games Played: {stats['games_played']}", True, white)
        games_rect = games_text.get_rect()
        games_rect.center = ((width / 2), 130)
        screen.blit(games_text, games_rect)
        
        wins_text = smallFont.render(f"Player Wins: {stats['player_wins']} ({int(stats['player_wins']/max(1, stats['games_played'])*100)}%)", True, green)
        wins_rect = wins_text.get_rect()
        wins_rect.center = ((width / 2), 155)
        screen.blit(wins_text, wins_rect)
        
        loss_text = smallFont.render(f"AI Wins: {stats['ai_wins']} ({int(stats['ai_wins']/max(1, stats['games_played'])*100)}%)", True, red)
        loss_rect = loss_text.get_rect()
        loss_rect.center = ((width / 2), 180)
        screen.blit(loss_text, loss_rect)
        
        tie_text = smallFont.render(f"Ties: {stats['ties']} ({int(stats['ties']/max(1, stats['games_played'])*100)}%)", True, white)
        tie_rect = tie_text.get_rect()
        tie_rect.center = ((width / 2), 205)
        screen.blit(tie_text, tie_rect)
        
        # Difficulty stats
        diff_title = mediumFont.render("Statistics by Difficulty", True, blue)
        diff_title_rect = diff_title.get_rect()
        diff_title_rect.center = ((width / 2), 245)
        screen.blit(diff_title, diff_title_rect)
        
        # Easy stats
        y_pos = 275
        for diff in [ttt.EASY, ttt.MEDIUM, ttt.HARD]:
            diff_stats = stats["by_difficulty"][diff]
            diff_games = diff_stats["games"]
            
            diff_text = smallFont.render(f"{diff.capitalize()}: {diff_games} games", True, white)
            diff_rect = diff_text.get_rect()
            diff_rect.center = ((width / 2), y_pos)
            screen.blit(diff_text, diff_rect)
            
            # Only show percentages if games have been played at this difficulty
            if diff_games > 0:
                player_win_pct = int(diff_stats["player_wins"] / diff_games * 100)
                ai_win_pct = int(diff_stats["ai_wins"] / diff_games * 100)
                tie_pct = int(diff_stats["ties"] / diff_games * 100)
                
                stats_text = smallFont.render(
                    f"Player: {player_win_pct}% | AI: {ai_win_pct}% | Ties: {tie_pct}%", 
                    True, 
                    white
                )
                stats_rect = stats_text.get_rect()
                stats_rect.center = ((width / 2), y_pos + 20)
                screen.blit(stats_text, stats_rect)
            
            y_pos += 45
        
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
                # If no user selected yet, go to the main menu
                if user is None:
                    pass
                # Otherwise return to the game
    
    # Let user choose a player and difficulty.
    elif user is None:

        # Draw title
        title = largeFont.render("Play Tic-Tac-Toe", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Draw buttons for X or O
        playXButton = pygame.Rect((width / 8), (height / 2) - 50, width / 4, 50)
        playX = mediumFont.render("Play as X", True, black)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, white, playXButton)
        screen.blit(playX, playXRect)

        playOButton = pygame.Rect(5 * (width / 8), (height / 2) - 50, width / 4, 50)
        playO = mediumFont.render("Play as O", True, black)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, white, playOButton)
        screen.blit(playO, playORect)
        
        # Draw difficulty selection buttons
        difficultyText = mediumFont.render("Select Difficulty:", True, white)
        difficultyRect = difficultyText.get_rect()
        difficultyRect.center = ((width / 2), (height / 2) + 30)
        screen.blit(difficultyText, difficultyRect)
        
        easyButton = pygame.Rect((width / 8), (height / 2) + 70, width / 5, 50)
        easy = mediumFont.render("Easy", True, black)
        easyRect = easy.get_rect()
        easyRect.center = easyButton.center
        pygame.draw.rect(screen, white, easyButton)
        screen.blit(easy, easyRect)
        
        mediumButton = pygame.Rect((width / 2) - (width / 10), (height / 2) + 70, width / 5, 50)
        medium = mediumFont.render("Medium", True, black)
        mediumRect = medium.get_rect()
        mediumRect.center = mediumButton.center
        pygame.draw.rect(screen, white, mediumButton)
        screen.blit(medium, mediumRect)
        
        hardButton = pygame.Rect(7 * (width / 10), (height / 2) + 70, width / 5, 50)
        hard = mediumFont.render("Hard", True, black)
        hardRect = hard.get_rect()
        hardRect.center = hardButton.center
        pygame.draw.rect(screen, white, hardButton)
        screen.blit(hard, hardRect)
        
        # Add Statistics button
        statsButton = pygame.Rect((width / 3), (height / 2) + 140, width / 3, 50)
        statsText = mediumFont.render("Statistics", True, black)
        statsRect = statsText.get_rect()
        statsRect.center = statsButton.center
        pygame.draw.rect(screen, white, statsButton)
        screen.blit(statsText, statsRect)
        
        # Display current selections
        if user is not None:
            userText = mediumFont.render(f"Player: {user}", True, white)
            userRect = userText.get_rect()
            userRect.center = ((width / 2), (height / 2) + 150)
            screen.blit(userText, userRect)
            
        if difficulty is not None:
            diffText = mediumFont.render(f"Difficulty: {difficulty.capitalize()}", True, white)
            diffRect = diffText.get_rect()
            diffRect.center = ((width / 2), (height / 2) + 180)
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
                
        # Start game once player and difficulty are selected
        if user is not None and difficulty is not None:
            time.sleep(0.5)  # Short delay before starting game
            # If user is O, AI goes first
            if user == ttt.O:
                ai_turn = True

    else:

        # Draw game board
        tile_size = 80
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
                pygame.draw.rect(screen, white, rect, 3)

                if board[i][j] != ttt.EMPTY:
                    move = moveFont.render(board[i][j], True, white)
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
            # Usamos una variable estática para marcar si ya actualizamos las estadísticas para este juego
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
                title = f"Game Over: {winner} wins."
        elif user == player_current:
            title = f"Play as {user}"
        else:
            title = f"Computer thinking..."
        title = largeFont.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)
        
        # Display current difficulty - Fix for NoneType error
        if difficulty is not None:
            diffText = mediumFont.render(f"Difficulty: {difficulty.capitalize()}", True, white)
            diffRect = diffText.get_rect()
            diffRect.center = ((width / 2), 70)
            screen.blit(diffText, diffRect)
        else:
            # Set a default difficulty if it somehow became None
            difficulty = ttt.MEDIUM
            diffText = mediumFont.render(f"Difficulty: {difficulty.capitalize()}", True, white)
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
            # Show buttons for play again and statistics
            againButton = pygame.Rect(width / 8, height - 65, width / 3, 50)
            again = mediumFont.render("Play Again", True, black)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton)
            screen.blit(again, againRect)
            
            statsButton = pygame.Rect(5 * width / 8, height - 65, width / 3, 50)
            statsText = mediumFont.render("Statistics", True, black)
            statsRect = statsText.get_rect()
            statsRect.center = statsButton.center
            pygame.draw.rect(screen, white, statsButton)
            screen.blit(statsText, statsRect)
            
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = ttt.initial_state()
                    ai_turn = False
                    difficulty = None
                elif statsButton.collidepoint(mouse):
                    time.sleep(0.2)
                    showing_stats = True
                    # Reload stats before showing
                    stats = ttt.load_stats()

    pygame.display.flip()
