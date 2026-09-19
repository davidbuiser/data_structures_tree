import hashlib

def sha256(data: str) -> str:
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

class MerkleTree:
    def __init__(self, transactions):
        self.transactions = transactions
        
    def _build_tree(self):
        if not self.transactions:
            return []
            
        current_ll = [sha256(tx) for tx in self.transactions]
        tree = [current_ll]
        
        while len(current_ll) > 1:
            if len(current_ll) % 2 != 0:
                current_ll.append(current_ll[-1])
                
            next_ll = []
            for i in range(0, len(current_ll), 2):
                combined = current_ll[i] + current_ll[i+1]
                next_ll.append(sha256(combined))
                
            tree.append(next_ll)
            current_ll = next_ll
            
        return tree

    def get_root(self):
        tree = self._build_tree()
        return tree[-1][0] if tree else None

    def get_proof(self, tx_index):
        tree = self._build_tree()
        proof = []
        idx = tx_index
        
        for ll in tree[:-1]:
            is_right_child = (idx % 2 == 1)
            sibling_idx = idx - 1 if is_right_child else idx + 1
            
            direction = 'L' if is_right_child else 'R'
            proof.append((ll[sibling_idx], direction))
            
            idx = idx // 2
            
        return proof

def verify_proof(tx_data, proof, root_hash):
    current_hash = sha256(tx_data)
    
    for sibling_hash, direction in proof:
        if direction == 'R':
            current_hash = sha256(current_hash + sibling_hash)
        else:
            current_hash = sha256(sibling_hash + current_hash)
            
    return current_hash == root_hash

if __name__ == "__main__":
    print("--- 1. Creando 5 transacciones simuladas ---")
    txs = ["Tx1: Abigail paga a Alexander 10", 
           "Tx2: Alexander paga a Mateo 5", 
           "Tx3: Mateo paga a Julián 2", 
           "Tx4: Julián paga a  8", 
           "Tx5:  paga a Abigail 3"]
           
    mt = MerkleTree(txs)
    
    print("\n--- 2. Construir árbol y mostrar Raíz ---")
    root1 = mt.get_root()
    print(f"Merkle Root original: {root1}")
    
    print("\n--- 3. Modificar una transacción ---")
    txs_modificadas = txs.copy()
    txs_modificadas[1] = "Tx2: Alexander paga a Mateo 500"
    mt_modificado = MerkleTree(txs_modificadas)
    root2 = mt_modificado.get_root()
    print(f"Nuevo Merkle Root:    {root2}")
    print(f"¿Las raíces son iguales? {root1 == root2} (Demuestra que la raíz cambió)")
    
    print("\n--- 4. Prueba de inclusión válida (Tx 3) ---")
    tx3_data = txs[2]
    print(f"Datos de la transacción 3: {tx3_data}")
    proof_tx3 = mt.get_proof(2)
    is_valid = verify_proof(tx3_data, proof_tx3, root1)
    print(f"Dato a verificar: '{tx3_data}'")
    print(f"¿Prueba Válida?: {is_valid}")
    
    print("\n--- 5. Prueba de inclusión con dato incorrecto ---")
    tx3_fake = "Tx3: Mateo paga a Julián 200"
    is_valid_fake = verify_proof(tx3_fake, proof_tx3, root1)
    print(f"Dato a verificar: '{tx3_fake}'")
    print(f"¿Prueba Válida?: {is_valid_fake} (Falla exitosamente)")