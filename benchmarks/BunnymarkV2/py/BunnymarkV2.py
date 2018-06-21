from godot import exposed
from godot.bindings import Node2D, Vector2, ResourceLoader, Sprite, Label, Node2D
from random import random

@exposed
class BunnymarkV2(Node2D):
	def _ready(self):
		self.grav = 500
		self.bunny_texture = ResourceLoader.load("res://images/godot_bunny.png")
		self.bunny_speeds = []
		self.label = Label()
		self.bunnies = Node2D()
		self.screen_size = self.get_viewport_rect().size

		self.add_child(self.bunnies)
		self.label.rect_position = Vector2(0, 20)
		self.add_child(self.label)

	def _process(self, delta):
		self.label.text = "Bunnies: " + str(self.bunnies.get_child_count())

		bunny_children = self.bunnies.get_children()
		for i in range(0, len(bunny_children)):
			bunny = bunny_children[i]
			pos = bunny.position
			speed = self.bunny_speeds[i]

			pos.x += speed.x * delta
			pos.y += speed.y * delta

			speed.y += self.grav * delta

			if pos.x > self.screen_size.x:
				speed.x *= -1
				pos.x = self.screen_size.x

			if pos.x < 0:
				speed.x *= -1
				pos.x = 0

			if pos.y > self.screen_size.y:
				pos.y = self.screen_size.y
				if random() > 0.5:
					speed.y = -(int(random() * 1100) + 50)
				else:
					speed.y *= -0.85

			if pos.y < 0:
				speed.y = 0
				pos.y = 0

			bunny.position = pos
			self.bunny_speeds[i] = speed

	def add_bunny(self):
		bunny = Sprite()
		bunny.set_texture(self.bunny_texture)
		self.bunnies.add_child(bunny)
		bunny.position = Vector2(self.screen_size.x / 2, self.screen_size.y / 2)
		self.bunny_speeds.append(Vector2(int(random() * 200) + 50, int(random() * 200) + 50))

	def remove_bunny(self):
		for _ in range(10):
			child_count = self.bunnies.get_child_count()
			if child_count == 0:
				return
			bunny = self.bunnies.get_child(child_count - 1)
			self.bunny_speeds.pop()
			self.bunnies.remove_child(bunny)

	def finish(self):
		emit_signal("benchmark_finished", self.bunnies.get_child_count())
