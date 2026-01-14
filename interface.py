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
        
        # COLONNE DROITE : ACTIONNEURS
        frame_actionneurs = tk.LabelFrame(
            frame_principal,
            text="⚙️ ACTIONNEURS (Sorties)",
            font=("Arial", 14, "bold"),
            bg='#34495e',
            fg='white',
            padx=15,
            pady=15
        )
        frame_actionneurs.grid(row=0, column=1, sticky='nsew', padx=5)
        
        self.boutons_actionneurs = {}
        
        # Actionneurs A8 (Z1-Z4)
        tk.Label(
            frame_actionneurs,
            text="Groupe A8 (Z1-Z4)",
            font=("Arial", 11, "bold"),
            bg='#34495e',
            fg='#e67e22'
        ).grid(row=0, column=0, columnspan=2, pady=5)
        
        actionneurs_a8 = [
            "Z1_ENTRER", "Z1_SORTIR", "Z2_ENTRER", "Z2_SORTIR",
            "Z3_ENTRER", "Z3_SORTIR", "Z4_ENTRER", "Z4_SORTIR"
        ]
        
        for i, nom in enumerate(actionneurs_a8):
            btn = tk.Button(
                frame_actionneurs,
                text=f"A8.{i}\n{nom}",
                font=("Arial", 9),
                bg='#95a5a6',
                fg='white',
                width=15,
                height=2,
                command=lambda a=8, b=i: self.toggle_actionneur(a, b)
            )
            btn.grid(row=i+1, column=0, pady=3, padx=5)
            self.boutons_actionneurs[f'A8.{i}'] = btn
        
        # Actionneurs A9 (Z5-Z8)
        tk.Label(
            frame_actionneurs,
            text="Groupe A9 (Z5-Z8)",
            font=("Arial", 11, "bold"),
            bg='#34495e',
            fg='#e67e22'
        ).grid(row=9, column=0, columnspan=2, pady=5)
        
        actionneurs_a9 = [
            "Z5_ENTRER", "Z5_SORTIR", "Z6_ENTRER", "Z6_SORTIR",
            "Z7_ENTRER", "Z7_SORTIR", "Z8_ENTRER", "Z8_SORTIR"
        ]
        
        for i, nom in enumerate(actionneurs_a9):
            btn = tk.Button(
                frame_actionneurs,
                text=f"A9.{i}\n{nom}",
                font=("Arial", 9),
                bg='#95a5a6',
                fg='white',
                width=15,
                height=2,
                command=lambda a=9, b=i: self.toggle_actionneur(a, b)
            )
            btn.grid(row=i+10, column=0, pady=3, padx=5)
            self.boutons_actionneurs[f'A9.{i}'] = btn
        
        # Configurer le redimensionnement
        frame_principal.columnconfigure(0, weight=1)
        frame_principal.columnconfigure(1, weight=1)
        frame_principal.rowconfigure(0, weight=1)
        
        # Boutons de contrôle en bas
        frame_controle = tk.Frame(self.fenetre, bg='#2c3e50')
        frame_controle.pack(fill='x', padx=20, pady=10)
        
        self.btn_surveillance = tk.Button(
            frame_controle,
            text="▶️ DÉMARRER SURVEILLANCE",
            font=("Arial", 12, "bold"),
            bg='#3498db',
            fg='white',
            command=self.toggle_surveillance,
            width=25
        )
        self.btn_surveillance.pack(side='left', padx=5)
        
        btn_rafraichir = tk.Button(
            frame_controle,
            text="🔄 RAFRAÎCHIR",
            font=("Arial", 12, "bold"),
            bg='#16a085',
            fg='white',
            command=self.rafraichir,
            width=15
        )
        btn_rafraichir.pack(side='left', padx=5)
        
        btn_quitter = tk.Button(
            frame_controle,
            text="❌ QUITTER",
            font=("Arial", 12, "bold"),
            bg='#e74c3c',
            fg='white',
            command=self.quitter,
            width=15
        )
        btn_quitter.pack(side='right', padx=5)
    
    def connecter(self):
        """Connecter à l'automate"""
        ip = self.entry_ip.get()
        
        try:
            client = snap7.client.Client()
            client.connect(ip, 0, 1)
            
            self.station = client
            self.label_statut.config(text="🟢 Connecté", fg='#27ae60')
            messagebox.showinfo("Succès", f"Connecté à {ip}")
            
            # Rafraîchir l'affichage
            self.rafraichir()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Connexion échouée : {e}")
    
    def rafraichir(self):
        """Lire et afficher l'état actuel"""
        if self.station is None:
            messagebox.showwarning("Attention", "Pas de connexion active")
            return
        
        try:
            # Lire capteurs
            data_e4 = self.station.eb_read(4, 1)
            data_e5 = self.station.eb_read(5, 1)
            
            # Mettre à jour affichage capteurs
            for i in range(8):
                bit_e4 = (data_e4[0] >> i) & 1
                bit_e5 = (data_e5[0] >> i) & 1
                
                self.labels_capteurs[f'E4.{i}'].config(
                    text="🟢" if bit_e4 else "⚪"
                )
                self.labels_capteurs[f'E5.{i}'].config(
                    text="🟢" if bit_e5 else "⚪"
                )
            
            # Lire actionneurs
            data_a8 = self.station.ab_read(8, 1)
            data_a9 = self.station.ab_read(9, 1)
            
            # Mettre à jour affichage actionneurs
            for i in range(8):
                bit_a8 = (data_a8[0] >> i) & 1
                bit_a9 = (data_a9[0] >> i) & 1
                
                self.boutons_actionneurs[f'A8.{i}'].config(
                    bg='#e74c3c' if bit_a8 else '#95a5a6'
                )
                self.boutons_actionneurs[f'A9.{i}'].config(
                    bg='#e74c3c' if bit_a9 else '#95a5a6'
                )
        
        except Exception as e:
            messagebox.showerror("Erreur", f"Lecture échouée : {e}")
    
