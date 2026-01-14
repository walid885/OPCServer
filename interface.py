#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
INTERFACE GRAPHIQUE SIMPLE
Pour contrôler la cellule flexible
"""

import tkinter as tk
from tkinter import ttk, messagebox
import snap7
import threading
import time

class InterfaceSupervision:
    def __init__(self):
        self.fenetre = tk.Tk()
        self.fenetre.title("🏭 Supervision Cellule Flexible")
        self.fenetre.geometry("900x700")
        self.fenetre.configure(bg='#2c3e50')
        
        # Variables
        self.station = None
        self.surveillance_active = False
        
        # Créer l'interface
        self.creer_interface()
        
    def creer_interface(self):
        """Créer tous les éléments visuels"""
        
        # Titre
        titre = tk.Label(
            self.fenetre,
            text="🏭 SUPERVISION CELLULE FLEXIBLE",
            font=("Arial", 20, "bold"),
            bg='#2c3e50',
            fg='white'
        )
        titre.pack(pady=20)
        
        # Frame de connexion
        frame_connexion = tk.Frame(self.fenetre, bg='#34495e', padx=20, pady=15)
        frame_connexion.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            frame_connexion,
            text="Adresse IP :",
            font=("Arial", 12),
            bg='#34495e',
            fg='white'
        ).grid(row=0, column=0, padx=5)
        
        self.entry_ip = tk.Entry(frame_connexion, font=("Arial", 12), width=20)
        self.entry_ip.insert(0, "172.16.1.3")
        self.entry_ip.grid(row=0, column=1, padx=5)
        
        self.btn_connecter = tk.Button(
            frame_connexion,
            text="🔌 CONNECTER",
            font=("Arial", 12, "bold"),
            bg='#27ae60',
            fg='white',
            command=self.connecter,
            width=15
        )
        self.btn_connecter.grid(row=0, column=2, padx=10)
        
        self.label_statut = tk.Label(
            frame_connexion,
            text="⚪ Déconnecté",
            font=("Arial", 12, "bold"),
            bg='#34495e',
            fg='#e74c3c'
        )
        self.label_statut.grid(row=0, column=3, padx=10)
        
        # Frame principale avec 2 colonnes
        frame_principal = tk.Frame(self.fenetre, bg='#2c3e50')
        frame_principal.pack(fill='both', expand=True, padx=20, pady=10)
        
        # COLONNE GAUCHE : CAPTEURS
        frame_capteurs = tk.LabelFrame(
            frame_principal,
            text="📊 CAPTEURS (Entrées)",
            font=("Arial", 14, "bold"),
            bg='#34495e',
            fg='white',
            padx=15,
            pady=15
        )
        frame_capteurs.grid(row=0, column=0, sticky='nsew', padx=5)
        
        self.labels_capteurs = {}
        
        # Capteurs E4 (S1-S8)
        tk.Label(
            frame_capteurs,
            text="Groupe E4 (S1-S8)",
            font=("Arial", 11, "bold"),
            bg='#34495e',
            fg='#3498db'
        ).grid(row=0, column=0, columnspan=2, pady=5)
        
        capteurs_e4 = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"]
        for i, nom in enumerate(capteurs_e4):
            tk.Label(
                frame_capteurs,
                text=f"E4.{i} ({nom})",
                font=("Arial", 10),
                bg='#34495e',
                fg='white'
            ).grid(row=i+1, column=0, sticky='w', pady=2)
            
            label = tk.Label(
                frame_capteurs,
                text="⚪",
                font=("Arial", 14),
                bg='#34495e'
            )
            label.grid(row=i+1, column=1, padx=10)
            self.labels_capteurs[f'E4.{i}'] = label
        
        # Capteurs E5 (S17, S18, S20, S21, S13-S16)
        tk.Label(
            frame_capteurs,
            text="Groupe E5 (S13-S21)",
            font=("Arial", 11, "bold"),
            bg='#34495e',
            fg='#3498db'
        ).grid(row=9, column=0, columnspan=2, pady=5)
        
        capteurs_e5 = ["S17", "S18", "S20", "S21", "S13", "S14", "S15", "S16"]
        for i, nom in enumerate(capteurs_e5):
            tk.Label(
                frame_capteurs,
                text=f"E5.{i} ({nom})",
                font=("Arial", 10),
                bg='#34495e',
                fg='white'
            ).grid(row=i+10, column=0, sticky='w', pady=2)
            
            label = tk.Label(
                frame_capteurs,
                text="⚪",
                font=("Arial", 14),
                bg='#34495e'
            )
            label.grid(row=i+10, column=1, padx=10)
            self.labels_capteurs[f'E5.{i}'] = label
        
