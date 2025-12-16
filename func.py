import argparse
import sys
from collections import deque
import random

import numpy as np

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Lab 10: Обход графа алгоритмом BFS',
        usage='python lab10.py [размер_графа] [стартовая_вершина] [взвешенность] [ориентация] [плотность]'
    )
    
    parser.add_argument('args', nargs='*', help='Аргументы в любом порядке')
    
    return parser.parse_args()

def smart_convert(value):
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value.lower()

def classify_and_identify_arguments(args):
    
    weighted_keywords = ['weighted', 'unweighted', 'взвешенный', 'невзвешенный']
    type_keywords = ['ori', 'unori', 'directed', 'undirected', 'ориентированный', 'неориентированный']
    
    result = {
        'graph_size': None,
        'start_vertex': None, 
        'weighted_mode': None,
        'graph_type': None,
        'density': None
    }
    
    # Сначала обрабатываем строковые аргументы (они однозначны)
    for arg in args:
        converted = smart_convert(arg)
        
        if isinstance(converted, str):
            if converted in weighted_keywords:
                if result['weighted_mode'] is None:
                    result['weighted_mode'] = 'weighted' if converted in ['weighted', 'взвешенный'] else 'unweighted'
            
            elif converted in type_keywords:
                if result['graph_type'] is None:
                    result['graph_type'] = 'ori' if converted in ['ori', 'directed', 'ориентированный'] else 'unori'
    
    # Теперь обрабатываем числа - пытаемся определить что есть что
    numbers = []
    floats = []
    
    for arg in args:
        converted = smart_convert(arg)
        
        if isinstance(converted, int):
            numbers.append(converted)
        elif isinstance(converted, float):
            floats.append(converted)
    
    # Обрабатываем плотность
    if floats:
        result['density'] = floats[0]  # берем первую плотность
    
    # Обрабатываем размер графа и стартовую вершину
    if len(numbers) >= 2:
        # Если есть два числа, большее будет размером графа, меньшее - стартовой вершиной
        # (но проверяем, что стартовая вершина не больше размера)
        max_num = max(numbers)
        min_num = min(numbers)
        
        # Если минимальное число может быть корректной стартовой вершиной для максимального
        if min_num < max_num:
            result['graph_size'] = max_num
            result['start_vertex'] = min_num
        else:
            # Иначе используем оба как размер и стартовую, но стартовая будет 0 если она >= размера
            result['graph_size'] = numbers[0]
            result['start_vertex'] = numbers[1] if numbers[1] < numbers[0] else 0
    
    elif len(numbers) == 1:
        # Если только одно число, это размер графа, стартовая вершина = 0
        result['graph_size'] = numbers[0]
        result['start_vertex'] = 0
    
    return result

def apply_defaults(params):
    defaults = {
        'graph_size': 5,
        'start_vertex': 0,
        'weighted_mode': 'unweighted',
        'graph_type': 'ori',
        'density': 0.5
    }
    
    result = {}
    for key in params:
        result[key] = params[key] if params[key] is not None else defaults[key]
    
    return result

def validate_graph_parameters(params):
    errors = []
    
    if params['graph_size'] < 1:
        errors.append("Размер графа должен быть положительным числом")
    
    if params['start_vertex'] < 0:
        errors.append("Стартовая вершина не может быть отрицательной")
    if params['start_vertex'] >= params['graph_size']:
        errors.append(f"Стартовая вершина {params['start_vertex']} должна быть в диапазоне [0, {params['graph_size']-1}]")
    
    if not (0.0 <= params['density'] <= 1.0):
        errors.append("Плотность графа должна быть в диапазоне [0.0, 1.0]")
    
    return errors

def generate_graph(size, is_weighted, is_directed, density):
    graph = [[0] * size for _ in range(size)]
    
    for i in range(size):
        for j in range(size):
            if i == j:
                continue
                
            if random.random() < density:
                if is_weighted:
                    weight = random.randint(1, 10)
                else:
                    weight = 1
                
                graph[i][j] = weight
                
                if not is_directed and i != j:
                    graph[j][i] = weight
    print(np.array(graph))
    return graph

def bfsd(G, v):
    q = deque()
    q.append(v)
    dist = [-1] * len(G)
    dist[v] = 0

    while q:
        v = q.popleft()
        for i in range(len(G)):
            if G[v][i] > 0 and dist[i] == -1:
                q.append(i)
                dist[i] = dist[v] + G[v][i]

    return dist

    

def print_current_config(params, args_count):
    is_directed = params['graph_type'] == 'ori'
    is_weighted = params['weighted_mode'] == 'weighted'
    
    print(f"\n Конфигурация графа:")
    print(f"  • {params['graph_size']} вершин")
    print(f"  • Стартовая вершина: {params['start_vertex']}")
    print(f"  • Тип: {'ориентированный' if is_directed else 'неориентированный'}")
    print(f"  • Взвешенность: {'взвешенный' if is_weighted else 'невзвешенный'}")
    print(f"  • Плотность: {params['density']:.2f}")
    
    if args_count < 5:
        print(f"  • Использовано аргументов: {args_count}/5")




def ecentrice(G):
    ecentrices = [0]*len(G)
    for i in range(len(G)):
        ecentrices[i] = max(bfsd(G, i))

    return ecentrices

def diametri(ecentices):
    diam = max(ecentices)
    return diam

def perif(ecentrices, diam):
    peripheral_vertices = []
    for i, ecc in enumerate(ecentrices):
        if ecc == diam:
            peripheral_vertices.append(i)
    return peripheral_vertices

def radiusi(ecentrices):
    return min(ecentrices)

def centr(eccentricities, radius):
    centers = []
    for idx, ecc in enumerate(eccentricities):
        if ecc == radius:
            centers.append(idx)
    return centers

#от она ↓
def gravity_center(graph):
    n = len(graph)
    total_distances = [0] * n
    
    for i in range(n):
        distances = bfsd(graph, i)
        total_distances[i] = sum(dist for dist in distances if dist != -1)

    min_distance = min(total_distances)

    gravity_centers = []
    for i, total in enumerate(total_distances):
        if total == min_distance:
            gravity_centers.append(i)
    
    return gravity_centers, total_distances, min_distance