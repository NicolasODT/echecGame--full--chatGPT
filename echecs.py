import chess
import pygame
import os
import random
import chess.engine
import pygame_gui
from pygame_gui.windows import UIConfirmationDialog

# Configuration de base
taille_case = 80
taille_echiquier = 8 * taille_case

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)

# Initialisation de pygame
pygame.init()

def init_ui(manager):
    # Sélection de la difficulté
    difficulty_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((taille_echiquier + 10, 100), (150, 40)), text="Difficulté", manager=manager)
    difficulty_dropdown = pygame_gui.elements.UIDropDownMenu(options_list=["Facile", "Moyen", "Difficile"], starting_option="Facile", relative_rect=pygame.Rect((taille_echiquier + 10, 140), (150, 40)), manager=manager)
    restart_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((taille_echiquier + 10, 200), (150, 40)), text="Redémarrer", manager=manager)

    return difficulty_dropdown, restart_button

def choisir_mouvement_bot(echiquier, profondeur):
    with chess.engine.SimpleEngine.popen_uci("stockfish") as engine:  # Remplacez "stockfish" par le chemin vers l'exécutable de Stockfish sur votre système
        result = engine.play(echiquier, chess.engine.Limit(depth=profondeur))
        meilleur_mouvement = result.move
    return meilleur_mouvement

def choisir_mouvement_bot(echiquier):
    mouvements_legaux = list(echiquier.legal_moves)
    return random.choice(mouvements_legaux)

restart_dialog = None

def dessiner_piece(screen, piece, x, y):
    piece_color = (220, 220, 220) if piece.color == chess.WHITE else (30, 30, 30)
    piece_type = piece.piece_type

    if piece_type == chess.PAWN:
        pygame.draw.circle(screen, piece_color, (x + taille_case // 2, y + taille_case // 2), taille_case // 4)
    elif piece_type == chess.KNIGHT:
        pygame.draw.polygon(screen, piece_color, [(x + taille_case // 2, y + taille_case // 4), (x + taille_case // 4, y + 3 * taille_case // 4), (x + 3 * taille_case // 4, y + 3 * taille_case // 4)])
    elif piece_type == chess.BISHOP:
        pygame.draw.polygon(screen, piece_color, [(x + taille_case // 2, y + taille_case // 4), (x + taille_case // 4, y + 3 * taille_case // 4), (x + 3 * taille_case // 4, y + 3 * taille_case // 4)])
        pygame.draw.circle(screen, piece_color, (x + taille_case // 2, y + taille_case // 4), taille_case // 8)
    elif piece_type == chess.ROOK:
        pygame.draw.rect(screen, piece_color, (x + taille_case // 4, y + taille_case // 4, taille_case // 2, taille_case // 2))
        pygame.draw.rect(screen, piece_color, (x + taille_case // 4, y + taille_case // 8, taille_case // 8, taille_case // 8))
        pygame.draw.rect(screen, piece_color, (x + 3 * taille_case // 8, y + taille_case // 8, taille_case // 8, taille_case // 8))
    elif piece_type == chess.QUEEN:
        pygame.draw.polygon(screen, piece_color, [(x + taille_case // 2, y + taille_case // 4), (x + taille_case // 4, y + 3 * taille_case // 4), (x + 3 * taille_case // 4, y + 3 * taille_case // 4)])
        pygame.draw.circle(screen, piece_color, (x + taille_case // 2, y + taille_case // 4), taille_case // 6)
        pygame.draw.circle(screen, piece_color, (x + taille_case // 2, y + taille_case // 2), taille_case // 8)
    elif piece_type == chess.KING:
        pygame.draw.rect(screen, piece_color, (x + taille_case // 4, y + taille_case // 4, taille_case // 2, taille_case // 2))
        pygame.draw.circle(screen, piece_color, (x + taille_case // 2, y + taille_case // 4), taille_case // 8)
        pygame.draw.line(screen, piece_color, (x + taille_case // 2, y + taille_case // 4), (x + taille_case // 2, y + taille_case // 8), 2)

def afficher_echiquier(screen, echiquier):
    for r in range(8):
        for c in range(8):
            rect = pygame.Rect(c * taille_case, r * taille_case, taille_case, taille_case)
            pygame.draw.rect(screen, BLANC if (r + c) % 2 == 0 else NOIR, rect)

            piece_square = 8 * (7 - r) + c
            if 0 <= piece_square < 64:
                piece = echiquier.piece_at(piece_square)
                if piece:
                    dessiner_piece(screen, piece, rect.x, rect.y)

def coordonnees_pixel_vers_case(pos):
    x, y = pos
    return x // taille_case, y // taille_case


def afficher_resultat(manager, resultat):
    message = ""
    if resultat == "1-0":
        message = "Vous avez gagné !"
    elif resultat == "0-1":
        message = "Vous avez perdu."
    elif resultat == "1/2-1/2":
        message = "Match nul."
    else:
        message = "Erreur : résultat inattendu."
    
    if message:
        resultat_dialog = UIConfirmationDialog(rect=pygame.Rect((taille_echiquier // 2 - 100, taille_echiquier // 2 - 50), (200, 100)), manager=manager, window_title="Résultat", action_long_desc=message, blocking=True)
        restart_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((taille_echiquier // 2 - 50, taille_echiquier // 2 + 20), (100, 30)), text="Redémarrer", manager=manager)
        return restart_button



def main():
    screen = pygame.display.set_mode((taille_echiquier + 200, taille_echiquier))
    pygame.display.set_caption("Jeu d'échecs")

    echiquier = chess.Board()

    running = True
    piece_selectionnee = None

    # Initialisation de l'interface utilisateur
    manager = pygame_gui.UIManager((taille_echiquier + 200, taille_echiquier))
    difficulty_dropdown, restart_button = init_ui(manager)

    clock = pygame.time.Clock()

    restart_dialog = None
    restart_result_button = None

    while running and not echiquier.is_game_over():
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            manager.process_events(event)

            # Gestion des événements de l'interface utilisateur
            if event.type == pygame.USEREVENT:
                if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    if event.ui_element == difficulty_dropdown:
                        restart_dialog = UIConfirmationDialog(rect=pygame.Rect((taille_echiquier // 2 - 100, taille_echiquier // 2 - 50), (200, 100)), manager=manager, window_title="Confirmation", action_long_desc="Voulez-vous redémarrer la partie avec le nouveau niveau de difficulté ?", blocking=True)
                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == restart_button:
                        restart_dialog = UIConfirmationDialog(rect=pygame.Rect((taille_echiquier // 2 - 100, taille_echiquier // 2 - 50), (200, 100)), manager=manager, window_title="Confirmation", action_long_desc="Voulez-vous redémarrer la partie ?", blocking=True)
                elif event.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    if restart_dialog:
                        echiquier = chess.Board()
                        piece_selectionnee = None
                        restart_dialog = None

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = coordonnees_pixel_vers_case(event.pos)

                    if piece_selectionnee:
                        if piece_selectionnee == (x, y):
                            piece_selectionnee = None
                        else:
                            mouvement = chess.Move.from_uci(chess.square_name(8 * (7 - piece_selectionnee[1]) + piece_selectionnee[0]) + chess.square_name(8 * (7 - y) + x))

                            if mouvement in echiquier.legal_moves:
                                echiquier.push(mouvement)
                                piece_selectionnee = None
                                if echiquier.is_game_over():
                                    restart_result_button = afficher_resultat(manager, echiquier.result())
                            elif echiquier.piece_at(8 * (7 - y) + x) and echiquier.color_at(8 * (7 - y) + x) == echiquier.turn:
                                piece_selectionnee = (x, y)
                    else:
                        if echiquier.piece_at(8 * (7 - y) + x) and echiquier.color_at(8 * (7 - y) + x) == echiquier.turn:
                            piece_selectionnee = (x, y)
            if echiquier.turn == chess.BLACK:
                profondeur_dict = {"Facile": 1, "Moyen": 3, "Difficile": 5}
                profondeur = profondeur_dict[difficulty_dropdown.selected_option]
                mouvement_bot = choisir_mouvement_bot(echiquier)
                echiquier.push(mouvement_bot)
                if echiquier.is_game_over():
                    restart_result_button = afficher_resultat(manager, echiquier.result())

        screen.fill((0, 0, 0))
        afficher_echiquier(screen, echiquier)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
