# LFA Exam · Castle of Illusions

Simulator de automat cu memorie și joc de aventură în terminal, realizate în Python pentru examenul la **Limbaje Formale și Automate (LFA)**, anul I, Facultatea de Matematică și Informatică, Universitatea din București.

**Examen de 24 de ore**

Acest repository păstrează lucrarea originală și o versiune revizuită pentru rulare și explorare. Nu conține enunțul examenului; explicațiile tehnice descriu implementarea disponibilă.

## Pornire

Necesită Python 3.10 sau mai nou. Nu sunt necesare biblioteci externe.

```bash
git clone https://github.com/AndreiasM5/lfa-exam.git
cd lfa-exam
python main.py
```

Pe Windows se poate folosi și `py main.py`. Configurațiile sunt găsite relativ la script, inclusiv atunci când îl pornești din alt director.

## Castle of Illusions

Explorezi camerele unui castel și colectezi obiectele care deblochează trecerile. Scopul este să ajungi la `Secret_Exit`.

| Comandă | Acțiune |
| --- | --- |
| `look` | Descrierea camerei, ieșiri și obiecte |
| `inventory` | Obiectele colectate |
| `take[key]` | Ridică un obiect |
| `drop[key]` | Lasă un obiect în camera curentă |
| `go[Armoury]` | Încearcă o trecere |
| `help` / `exit` | Ajutor / închidere |

Exemplu complet de evadare:

```text
take[key]
go[Armoury]
take[sword]
go[Treasury]
take[ancient_coin]
go[Library]
go[Secret_Exit]
```

## Simulatorul

`LA.py` citește secțiunile `[Sigma]`, `[Gamma]`, `[State]` și `[Delta]`. Marcajele stărilor sunt `0` pentru inițială și `2` pentru finală. Memoria este o colecție de simboluri distincte, nu o stivă clasică.

```text
origine, simbol_intrare, simbol_necesar, -> (destinatie, simbol_eliminat, simbol_adaugat)
```

`epsilon` indică absența unui simbol sau a unei operații. Căutarea urmărește starea, poziția în intrare și conținutul memoriei; acceptarea cere consumarea întregii intrări și atingerea unei stări finale.

**Configurația `LA_config.txt` este păstrată exact ca în original.** Primele tranziții cer eliminarea unui simbol din memoria inițial goală, deci nu sunt aplicabile. În consecință, exemplele `""` și `"xy"` sunt respinse. Nu am modificat configurația pentru a presupune o altă intenție fără enunț.

## Revizuire și verificare

- Corectate comenzile simple care provocau `IndexError`, comenzile invalide și închiderea intrării.
- Verificarea obiectului necesar folosește exact trecerea solicitată.
- Uniformizate numele `chef's_hat` și `spell_book`; adăugate inventarul și mesajul de evadare.
- Citire UTF-8 explicită, eliminarea spațiilor din configurație și validarea simbolului adăugat în memorie.
- Căutarea automatului distinge configurațiile cu memorii diferite și tratează tranzițiile epsilon, inclusiv ciclurile și pașii de după ultimul caracter.
- Importarea `main` nu pornește jocul.

```bash
python -m unittest discover -v
```

Verificat cu Python 3.12.14: **10 teste automate** pentru comenzi, inventar, acces blocat, evadare completă, configurația originală, tranziții epsilon și ramuri cu memorii diferite. Jocul a fost rulat și prin intrare standard. Aceste verificări nu înlocuiesc o evaluare față de enunțul original, care nu este inclus.

## Fișiere

| Fișier | Rol |
| --- | --- |
| `main.py` | Pornire |
| `LA.py` | Parser și simulator |
| `Game.py` | Joc interactiv |
| `*_config.txt` | Definițiile automatului și castelului |
| `test_exam.py` | Teste de regresie |
| `original/` | Cele cinci fișiere originale, nemodificate |

Autor: **Ivașcu Ioan-Andrei**, grupa 143 la momentul examenului.
