import pygame
import sys

# Initialiser Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_icon(pygame.image.load("icon.png"))
pygame.display.set_caption("Connexion")

# Couleurs personnalisées
BACKGROUND_TOP = (16, 185, 129)  # Vert émeraude
BACKGROUND_BOTTOM = (37, 99, 235)  # Bleu
CARD_COLOR = (15, 23, 42, 200)  # Carte semi-transparente
BORDER_COLOR = (255, 255, 255)  # Blanc
PRIMARY_COLOR = (22, 163, 74)  # Bouton vert foncé
TEXT_COLOR = (255, 255, 255)  # Texte blanc
INPUT_COLOR = (50, 50, 60)  # Champs normaux
INPUT_ACTIVE_COLOR = (70, 70, 80)  # Champs actifs
ERROR_COLOR = (255, 69, 58)  # Rouge vif pour les erreurs
SUCCESS_COLOR = (129, 236, 236)  # Bleu clair pour succès

# Police
font = pygame.font.Font(None, 32)
title_font = pygame.font.Font(None, 50)

# Variables de texte
username_text = ""
password_text = ""
active_username = False
active_password = False
login_message = ""
login_color = ERROR_COLOR  # Couleur du message par défaut

# Espacement des champs et boutons
field_spacing = 60  # Plus grand espacement pour éviter les chevauchements

# Responsiveness - Calcul des dimensions dynamiques
def resize_layout(width, height):
    global username_rect, password_rect, button_rect, title_pos, card_rect, message_pos
    margin_x, margin_y = width // 6, height // 4

    # Dimensions de la carte
    card_width, card_height = width - 2 * margin_x, 360
    card_rect = pygame.Rect(margin_x, margin_y, card_width, card_height)

    # Centrer les éléments sur la carte avec espacement fixe
    username_rect = pygame.Rect(card_rect.x + 40, card_rect.y + 80, card_width - 80, 40)
    password_rect = pygame.Rect(card_rect.x + 40, username_rect.y + field_spacing, card_width - 80, 40)
    button_rect = pygame.Rect(card_rect.x + 40, password_rect.y + field_spacing, card_width - 80, 40)
    title_pos = (width // 2, card_rect.y + 30)

    # Position du message de connexion
    message_pos = (card_rect.centerx, button_rect.y + field_spacing)

resize_layout(WIDTH, HEIGHT)

# Dessiner un fond dégradé
def draw_gradient(surface, color1, color2, width, height):
    for y in range(height):
        blend_ratio = y / height
        blended_color = (
            int(color1[0] * (1 - blend_ratio) + color2[0] * blend_ratio),
            int(color1[1] * (1 - blend_ratio) + color2[1] * blend_ratio),
            int(color1[2] * (1 - blend_ratio) + color2[2] * blend_ratio),
        )
        pygame.draw.line(surface, blended_color, (0, y), (width, y))

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Gestion du redimensionnement
        if event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.size
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            resize_layout(WIDTH, HEIGHT)

        # Gestion des clics de souris
        if event.type == pygame.MOUSEBUTTONDOWN:
            active_username = username_rect.collidepoint(event.pos)
            active_password = password_rect.collidepoint(event.pos)

            if button_rect.collidepoint(event.pos):
                if username_text and password_text:
                    login_message = "Connexion réussie !"
                    login_color = SUCCESS_COLOR
                else:
                    login_message = "Veuillez remplir tous les champs."
                    login_color = ERROR_COLOR

        # Gestion du clavier
        if event.type == pygame.KEYDOWN:
            if active_username:
                if event.key == pygame.K_BACKSPACE:
                    username_text = username_text[:-1]
                else:
                    username_text += event.unicode

            if active_password:
                if event.key == pygame.K_BACKSPACE:
                    password_text = password_text[:-1]
                else:
                    password_text += event.unicode

    # Dessiner l'interface
    draw_gradient(screen, BACKGROUND_TOP, BACKGROUND_BOTTOM, WIDTH, HEIGHT)

    # Dessiner la carte
    card_surface = pygame.Surface((card_rect.width, card_rect.height), pygame.SRCALPHA)
    pygame.draw.rect(card_surface, CARD_COLOR, (0, 0, card_rect.width, card_rect.height), border_radius=20)
    screen.blit(card_surface, (card_rect.x, card_rect.y))

    # Bord de la carte
    pygame.draw.rect(screen, BORDER_COLOR, card_rect, width=2, border_radius=20)

    # Titre
    title_surface = title_font.render("Connexion", True, TEXT_COLOR)
    title_rect = title_surface.get_rect(center=title_pos)
    screen.blit(title_surface, title_rect)

    # Champs de texte
    pygame.draw.rect(screen, INPUT_ACTIVE_COLOR if active_username else INPUT_COLOR, username_rect, border_radius=5)
    pygame.draw.rect(screen, INPUT_ACTIVE_COLOR if active_password else INPUT_COLOR, password_rect, border_radius=5)

    # Texte des champs
    username_surface = font.render(username_text, True, TEXT_COLOR)
    password_surface = font.render('*' * len(password_text), True, TEXT_COLOR)
    screen.blit(username_surface, (username_rect.x + 10, username_rect.y + 10))
    screen.blit(password_surface, (password_rect.x + 10, password_rect.y + 10))

    # Libellés des champs
    username_label = font.render("Nom d'utilisateur", True, TEXT_COLOR)
    password_label = font.render("Mot de passe", True, TEXT_COLOR)
    screen.blit(username_label, (username_rect.x, username_rect.y - 30))
    screen.blit(password_label, (password_rect.x, password_rect.y - 30))

    # Bouton de connexion
    pygame.draw.rect(screen, PRIMARY_COLOR, button_rect, border_radius=5)
    button_text = font.render("Se connecter", True, TEXT_COLOR)
    button_rect_text = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_rect_text)

    # Message de connexion dans la carte
    if login_message:
        message_surface = font.render(login_message, True, login_color)
        screen.blit(message_surface, message_surface.get_rect(center=message_pos))

    # Mise à jour de l'écran
    pygame.display.flip()

pygame.quit()
sys.exit()
