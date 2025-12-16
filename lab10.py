from func import *

def main():
    try:
        args = parse_arguments()
        
        identified_params = classify_and_identify_arguments(args.args)
        final_params = apply_defaults(identified_params)
        
        validation_errors = validate_graph_parameters(final_params)
        if validation_errors:
            print("Ошибки в параметрах графа:")
            for error in validation_errors:
                print(f"  • {error}")
            
            sys.exit(1)
        
        print_current_config(final_params, len(args.args))
        
        is_directed = final_params['graph_type'] == 'ori'
        is_weighted = final_params['weighted_mode'] == 'weighted'
        
        print(f"\n Генерация графа...")
        graph = generate_graph(
            size=final_params['graph_size'],
            is_weighted=is_weighted,
            is_directed=is_directed,
            density=final_params['density']
        )
        
        
        distances = [0]*len(graph)
        ecentrices = [0]*len(graph)

        for i in range(len(graph)):
            distances[i] = bfsd(graph, i)
            ecentrices[i] = max(distances[i])

        
        print(f"\nМатрица расстояний:\n{np.array(distances)}\n")
        print(f"Эксцентриситеты\n{np.array(ecentrices)}")
    
        radius = min(ecentrices) if min(ecentrices) != 0 else None
        print(f"Радиус: {radius}, центральная вершина: {centr(ecentrices, radiusi(ecentrices))}")

        diametr = max(ecentrices) if max(ecentrices) != 0 else None
        print(f"Диаметр: {diametr}, Периферийные вершина: {perif(ecentrices, diametri(ecentrices))}")
        
        # Поиск центра тяжести гарфа
        gravity_centers, total_distances, min_distance = gravity_center(graph)
        print(f"\nЦентр тяжести графа = {min_distance}: {gravity_centers}")
        print(f"Суммы расстояний от каждой вершины до всех других:")
        for i, total in enumerate(total_distances):
            print(f"  Вершина {i}: {total}")

    except Exception as e:
        print(f"Ошибочка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()