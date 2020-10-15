import torch
import numpy as np
import random
from collections import namedtuple, deque

class ReplayBuffer:
	def __init__(self, buffer_size, batch_size, device):
		self.memory = deque(maxlen=buffer_size)
		self.batch_size = batch_size
		self.experience = namedtuple("Experience", field_names=["state","action","reward","next_state","done"])
		self.device = device

	def remember(self, state, action, reward, next_state, done):
		single_memory = self.experience(state, action, reward, next_state, done)
		self.memory.append(single_memory)

	def retrieve(self):
		experiences = random.sample(self.memory, k=self.batch_size)

		states = torch.from_numpy(np.vstack([e.state for e in experiences if e is not None])).float().to(self.device)
		actions = torch.from_numpy(np.vstack([e.action for e in experiences if e is not None])).float().to(self.device)
		rewards = torch.from_numpy(np.vstack([e.reward for e in experiences if e is not None])).float().to(self.device)
		next_states = torch.from_numpy(np.vstack([e.next_state for e in experiences if e is not None])).float().to(self.device)
		dones = torch.from_numpy(np.vstack([e.done for e in experiences if e is not None]).astype(np.uint8)).float().to(self.device)

		return (states, actions, rewards, next_states, dones)
	
	def __len__(self):
		"""Return the current size of internal memory."""
		return len(self.memory)