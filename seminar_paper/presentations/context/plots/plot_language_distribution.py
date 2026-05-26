import matplotlib.pyplot as plt

# Data
languages = [
    "C",
    "C++",
    "Python",
    "Java",
    "JavaScript",
    "PHP",
    "Go",
    "Ruby",
    "Verilog",
    "HTML",
    "TypeScript",
    "Rust",
]

values = [10, 5, 13, 5, 5, 1, 1, 1, 1, 1, 1, 0]

total = 21

# Sort
languages, values = zip(*sorted(zip(languages, values), key=lambda x: x[1]))

plt.figure(figsize=(12, 5))

# Create colors (red for Rust, default for others)
colors = ["red" if lang == "Rust" else "#5B8FF9" for lang in languages]

bars = plt.barh(
    languages,
    values,
    height=0.6,
    color=colors,
    edgecolor="black"
)

# Labels
for bar, value, lang in zip(bars, values, languages):
    percent = value / total * 100
    text_color = "red" if lang == "Rust" else "black"

    plt.text(
        value + 0.25,
        bar.get_y() + bar.get_height() / 2,
        f"{percent:.1f}%",
        va="center",
        fontsize=16,
        color=text_color
    )

# Styling
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

ax = plt.gca()

for tick_label in ax.get_yticklabels():
    if tick_label.get_text() == "Rust":
        tick_label.set_color("red")

plt.grid(axis="x", linestyle="--", alpha=0.6)
plt.gca().invert_yaxis()

plt.gca().spines["top"].set_visible(False)
plt.gca().spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig("programming_language_distribution.png", dpi=300, bbox_inches="tight")
plt.show()