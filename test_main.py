import main
import unittest
import os
import unittest
import tkinter as tk
from lsb_package import StartPage, TranscriptionPage, KeywordsPage, LlmPage

class TestApp(unittest.TestCase):
	def setUp(self):
		self.app = main.App()

	def test_appExists(self):
		self.assertIsNotNone(self.app)

	def test_init_title(self):
		self.assertEqual(self.app.title(), "Lecture Summary Bot")

	def test_init_frames(self):
		for F in [StartPage, TranscriptionPage, KeywordsPage, LlmPage]:
			frame_name = str(F)
			self.assertIn(str(frame_name), {str(k): v for k, v in self.app.frames.items()})




if __name__ == "__main__":
    unittest.main()

