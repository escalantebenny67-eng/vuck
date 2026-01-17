import pygame

pygame.init()
screen = pygame.display.set_mode((800,600))
font = pygame.font.SysFont("Arial", 18, bold=True)
clock = pygame.time.Clock()

# constants
running = True
products = []
card_w, card_h = 200, 150
margin = 20
cols = 3
dragging = False
mouse_y_offset = 0
content_y_offset = 0
total_content_height = 0

# colors
black = (0,0,0)

# rects
track = pygame.Rect(780, 0, 20, 600)
handle = pygame.Rect(780, 0, 20, 80)

# functions
def add_card(name, price):
  # Create a dictionary for the new product
  new_product = {
    "name": name,
    "price": f"${price}",
    "color": (100, 100, 255)
  }
  products.append(new_product)
  total_rows = (len(products) + cols - 1) // cols
  total_content_height = total_rows * (card_h + margin) + 100
  return total_content_height,products
  
def draw_cards(screen, font, card_w, card_h, content_y_offset):
  global cols
  for i, item in enumerate(products):
    row = i // cols
    col = i % cols
        
    # Position math
    x = 50 + col * (card_w + margin)
    y = 50 + row * (card_h + margin) + content_y_offset
        
    if -card_h < y < 600:
      product_rect = pygame.Rect(x, y, card_w, card_h)
      pygame.draw.rect(screen, (30, 30, 30), product_rect, border_radius=10)
      name_surf = font.render(item['name'], True, (255, 255, 255))
      price_surf = font.render(item['price'], True, (0, 255, 100))
      screen.blit(name_surf, (x + 10, y + 20))
      screen.blit(price_surf, (x + 10, y + card_h - 30))
      
def scrollbar_event(event, handle):
  global dragging,mouse_y_offset
  if event.type == pygame.MOUSEBUTTONDOWN:
    if handle.collidepoint(event.pos):
      dragging = True
      mouse_y_offset = handle.y - event.pos[1]
                
  if event.type == pygame.MOUSEBUTTONUP:
    dragging = False

def scrollbar_logic(handle_rect, track_rect, total_h):
  global dragging, mouse_y_offset
  if dragging:
    handle_rect.y = pygame.mouse.get_pos()[1] + mouse_y_offset
    handle_rect.y = max(track_rect.top, min(handle_rect.y, track_rect.bottom - handle_rect.height))
        
    scroll_range = track_rect.height - handle_rect.height
    if scroll_range > 0:
      scroll_percent = (handle_rect.y - track_rect.top) / scroll_range
      return -(scroll_percent * (total_h - 600)) # Return the new offset
  return content_y_offset
  
# create pre-sets
for i in range(15):
  total_content_height, _ = add_card(f"Vuck Item {i+1}", (i+1)*5)
  
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    scrollbar_event(event,handle)
  
  content_y_offset = scrollbar_logic(handle, track, total_content_height)
  
  screen.fill(black)
  draw_cards(screen, font, card_w, card_h, content_y_offset)
  pygame.draw.rect(screen, (40, 40, 40), track)
  pygame.draw.rect(screen, (100, 100, 100), handle, border_radius=10)
  
  pygame.display.flip()
  clock.tick(60)
pygame.display.quit()
