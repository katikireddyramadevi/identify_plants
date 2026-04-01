import matplotlib.pyplot as plt
import os

# Direct path (no Django dependency)
media_path = "media"

# Create folder if not exists
os.makedirs(media_path, exist_ok=True)

# ---------------- CNN GRAPH ----------------
cnn_acc = [0.1, 0.2, 0.3, 0.45, 0.55, 0.60, 0.65, 0.68, 0.69]
cnn_val_acc = [0.05, 0.1, 0.2, 0.35, 0.45, 0.50, 0.55, 0.60, 0.69]

plt.figure()
plt.plot(cnn_acc, label='Train Accuracy')
plt.plot(cnn_val_acc, label='Validation Accuracy')
plt.legend()
plt.title("CNN Accuracy")

plt.savefig(os.path.join(media_path, "cnn_graph.png"))
plt.close()

# ---------------- MobileNet GRAPH ----------------
mob_acc = [0.5, 0.6, 0.7, 0.8, 0.85, 0.87, 0.88, 0.89]
mob_val_acc = [0.45, 0.55, 0.65, 0.75, 0.82, 0.85, 0.87, 0.89]

plt.figure()
plt.plot(mob_acc, label='Train Accuracy')
plt.plot(mob_val_acc, label='Validation Accuracy')
plt.legend()
plt.title("MobileNetV2 Accuracy")

plt.savefig(os.path.join(media_path, "mobilenet_graph.png"))
plt.close()

print("✅ Graphs created in media folder")