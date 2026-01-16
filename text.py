class Text:
  def __init__(self,text,style):
    self.text = text
    self.style = style
    self.colors = {
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "reset": "\033[0m"
    }
    self.bg_colors = {
      "red": "\033[41m",
      "green": "\033[42m",
      "blue": "\033[43m"
    }
    self.lists = {}  # store multiple lists by name
    self.size = 12
    self.color = None

  def parargraph(self,content):
    return f"\n{content}\n"

  def bold(self):
    return f"\033[1m{self.text}\033[0m"

  def italic(self):
    return f"\x1B[3m{self.text}\x1B[0m"

  def underline(self):
    return f"\x1b[4m{self.text}\x1b[0m"

  def setColor(self, color):
    if color in self.colors:
      return f"{self.colors[color]}{self.text}{self.colors['reset']}"
    else:
      return "invalid color"

  def highlight(self,color,inner_color):
    if color in self.colors:
      return f"{self.colors[color]}{self.bg_colors[inner_color]}{self.text}{self.colors['reset']}"
    else:
      return "invalid color"

  def bulletList(self, name,list_type="circle", content=None, indent=2, ordered=True):
    if name not in self.lists:
      self.lists[name] = {
        "items": content or [],
        "ordered": ordered,
        "indent": indent,
        "type": list_type
      }
      return self.render_list(name)

  def render_list(self, name):
    lst = self.lists[name]
    lines = []
    for i, item in enumerate(lst["items"], start=1):
      bullet = self.get_bullet(i, lst["type"])
      lines.append(" " * lst["indent"] + f"{bullet} {item}")
    return "\n".join(lines)

  def get_bullet(self, index, list_type):
    #Defines how each bullet is represented.
    match list_type:
      case "number":
        return f"{index}."
      case "alpha":
        return f"{chr(96 + index)}."
      case "circle":
        return "●"
      case "arrow":
        return "➤"
      case "dash":
        return "-"
      case "star":
        return "★"
      case None:
        return "-"

  def add_item(self, name, item):
    self.lists[name]["items"].append(item)

  def edit_item(self, name, index, new_item):
    self.lists[name]["items"][index] = new_item

  def remove_item(self, name, index):
    self.lists[name]["items"].pop(index)
