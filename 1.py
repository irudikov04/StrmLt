import numpy as np
import matplotlib.pyplot as plt

class SimpleNeuralNetwork:
    def __init__(self, input_size=1, hidden_size=3, output_size=1, learning_rate=0.01):
        """
        Простая нейронная сеть с одним скрытым слоем
        
        Параметры:
        input_size: количество входных нейронов
        hidden_size: количество нейронов в скрытом слое
        output_size: количество выходных нейронов
        learning_rate: скорость обучения
        """
        # Инициализация весов и смещений
        self.W1 = np.random.randn(input_size, hidden_size) * 0.01
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) * 0.01
        self.b2 = np.zeros((1, output_size))
        
        self.learning_rate = learning_rate
        self.loss_history = []
    
    def relu(self, x):
        """Функция активации ReLU"""
        return np.maximum(0, x)
    
    def relu_derivative(self, x):
        """Производная ReLU"""
        return (x > 0).astype(float)
    
    def forward(self, X):
        """
        Прямой проход через сеть
        """
        # Скрытый слой
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self.relu(self.z1)
        
        # Выходной слой (линейная активация для регрессии)
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        return self.z2
    
    def compute_loss(self, y_pred, y_true):
        """Среднеквадратичная ошибка"""
        return np.mean((y_pred - y_true) ** 2)
    
    def backward(self, X, y_true, y_pred):
        """
        Обратное распространение ошибки
        """
        m = X.shape[0]
        
        # Градиенты выходного слоя
        dz2 = 2 * (y_pred - y_true) / m
        dW2 = np.dot(self.a1.T, dz2)
        db2 = np.sum(dz2, axis=0, keepdims=True)
        
        # Градиенты скрытого слоя
        dz1 = np.dot(dz2, self.W2.T) * self.relu_derivative(self.z1)
        dW1 = np.dot(X.T, dz1)
        db1 = np.sum(dz1, axis=0, keepdims=True)
        
        return dW1, db1, dW2, db2
    
    def update_parameters(self, dW1, db1, dW2, db2):
        """Обновление весов"""
        self.W1 -= self.learning_rate * dW1
        self.b1 -= self.learning_rate * db1
        self.W2 -= self.learning_rate * dW2
        self.b2 -= self.learning_rate * db2
    
    def train(self, X, y, epochs=1000, verbose=True):
        """Обучение сети"""
        for epoch in range(epochs):
            # Прямой проход
            y_pred = self.forward(X)
            
            # Вычисление потерь
            loss = self.compute_loss(y_pred, y)
            self.loss_history.append(loss)
            
            # Обратное распространение
            dW1, db1, dW2, db2 = self.backward(X, y, y_pred)
            
            # Обновление параметров
            self.update_parameters(dW1, db1, dW2, db2)
            
            if verbose and epoch % 100 == 0:
                print(f"Эпоха {epoch}: Loss = {loss:.6f}")
    
    def predict(self, X):
        """Предсказание"""
        return self.forward(X)

# Пример использования для нелинейной задачи
def generate_nonlinear_data(n_samples=200):
    """Генерация нелинейных данных"""
    np.random.seed(42)
    X = np.random.randn(n_samples, 1) * 2
    y = np.sin(X * 2) + 0.5 * X + np.random.randn(n_samples, 1) * 0.1
    return X, y

def main():
    # Генерация данных
    X, y = generate_nonlinear_data(300)
    
    # Создание нейронной сети
    nn = SimpleNeuralNetwork(
        input_size=1,
        hidden_size=10,  # 10 нейронов в скрытом слое
        output_size=1,
        learning_rate=0.01
    )
    
    print("Архитектура сети:")
    print(f"Входной слой: {nn.W1.shape[0]} нейрон(ов)")
    print(f"Скрытый слой: {nn.W1.shape[1]} нейронов")
    print(f"Выходной слой: {nn.W2.shape[1]} нейрон(ов)")
    print("\nНачало обучения...")
    
    # Обучение
    nn.train(X, y, epochs=2000, verbose=True)
    
    # Визуализация
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    # 1. Данные и предсказания
    axes[0].scatter(X, y, alpha=0.5, s=10, label='Данные')
    X_test = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
    y_pred = nn.predict(X_test)
    axes[0].plot(X_test, y_pred, 'r-', linewidth=2, label='Предсказание сети')
    axes[0].set_xlabel('X')
    axes[0].set_ylabel('y')
    axes[0].set_title('Нейронная сеть: Данные и предсказание')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # 2. График потерь
    axes[1].plot(nn.loss_history)
    axes[1].set_xlabel('Эпоха')
    axes[1].set_ylabel('Потери (MSE)')
    axes[1].set_title('График обучения')
    axes[1].set_yscale('log')
    axes[1].grid(True, alpha=0.3)
    
    # 3. Активации нейронов скрытого слоя
    axes[2].set_title('Активации нейронов скрытого слоя')
    z1 = np.dot(X_test, nn.W1) + nn.b1
    for i in range(nn.W1.shape[1]):
        activation = nn.relu(z1[:, i:i+1])
        axes[2].plot(X_test, activation, alpha=0.7, label=f'Нейрон {i+1}')
    axes[2].set_xlabel('X')
    axes[2].set_ylabel('Активация')
    axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    print("\nПример предсказаний:")
    test_points = np.array([[-2], [0], [2]])
    predictions = nn.predict(test_points)
    for i, (x, pred) in enumerate(zip(test_points, predictions)):
        print(f"X = {x[0]:.1f}, Предсказание = {pred[0]:.3f}")

if __name__ == "__main__":
    main()