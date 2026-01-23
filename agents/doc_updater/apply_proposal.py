#!/usr/bin/env python3
"""
Script para aplicar o rechazar propuestas de actualización de documentación.

Uso:
    python apply_proposal.py <US-ID> --approve    # Aplica los cambios y mueve US a release
    python apply_proposal.py <US-ID> --reject     # Rechaza la propuesta
    python apply_proposal.py <US-ID> --status     # Muestra estado de la propuesta
"""

import os
import sys
import json
import shutil
from datetime import datetime

PROPOSALS_PATH = "../../docs/proposals"
BACKLOG_DONE_PATH = "../../docs/backlog/done"
RELEASES_PATH = "../../docs/releases"
APPLIED_LOG = "../../docs/proposals/.applied_proposals.json"


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def load_applied_log():
    """Carga el log de propuestas aplicadas"""
    if os.path.exists(APPLIED_LOG):
        with open(APPLIED_LOG, "r") as f:
            return json.load(f)
    return {}


def save_applied_log(log):
    """Guarda el log de propuestas aplicadas"""
    with open(APPLIED_LOG, "w") as f:
        json.dump(log, f, indent=2)


def get_proposal_path(us_id):
    """Obtiene la ruta de la propuesta"""
    return os.path.join(PROPOSALS_PATH, f"{us_id}_service_changes.md")


def get_us_path(us_id):
    """Obtiene la ruta de la US en done/"""
    for filename in os.listdir(BACKLOG_DONE_PATH):
        if filename.startswith(us_id):
            return os.path.join(BACKLOG_DONE_PATH, filename)
    return None


def approve_proposal(us_id):
    """
    Aprueba una propuesta.
    NOTA: Esta versión NO aplica cambios automáticamente.
    Los cambios deben aplicarse manualmente siguiendo la propuesta.
    """
    proposal_path = get_proposal_path(us_id)
    us_path = get_us_path(us_id)
    
    if not os.path.exists(proposal_path):
        print(f"❌ No se encuentra la propuesta: {proposal_path}")
        return False
    
    if not us_path:
        print(f"❌ No se encuentra la US {us_id} en {BACKLOG_DONE_PATH}")
        return False
    
    print(f"\n{'='*60}")
    print(f"📋 APROBANDO PROPUESTA: {us_id}")
    print(f"{'='*60}\n")
    
    # Mostrar la propuesta
    proposal_content = read_file(proposal_path)
    print("📄 Contenido de la propuesta:")
    print("-" * 60)
    print(proposal_content)
    print("-" * 60)
    
    # Confirmar
    print("\n⚠️  IMPORTANTE:")
    print("   Los cambios en services/ deben aplicarse MANUALMENTE siguiendo la propuesta.")
    print("   Este script solo registra la aprobación y archiva los documentos.\n")
    
    confirm = input("¿Confirmas que has aplicado los cambios manualmente? (yes/no): ")
    
    if confirm.lower() not in ['yes', 'y', 'sí', 'si']:
        print("❌ Operación cancelada")
        return False
    
    # Registrar aprobación
    log = load_applied_log()
    log[us_id] = {
        "approved_at": datetime.now().isoformat(),
        "proposal_file": f"{us_id}_service_changes.md",
        "us_file": os.path.basename(us_path),
        "status": "approved_manual"
    }
    save_applied_log(log)
    
    # Archivar propuesta (mover a carpeta archive)
    archive_path = os.path.join(PROPOSALS_PATH, "archive")
    os.makedirs(archive_path, exist_ok=True)
    archived_proposal = os.path.join(archive_path, f"{us_id}_service_changes.md")
    shutil.move(proposal_path, archived_proposal)
    
    print(f"\n✅ Propuesta aprobada y archivada")
    print(f"📁 Propuesta archivada en: {archived_proposal}")
    print(f"📝 US permanece en: {us_path}")
    print(f"\n💡 Próximos pasos:")
    print(f"   1. Verifica que los cambios en services/ estén correctos")
    print(f"   2. Mueve la US a la release correspondiente:")
    print(f"      mv {us_path} docs/releases/release-X.X/")
    
    return True


def reject_proposal(us_id):
    """Rechaza una propuesta"""
    proposal_path = get_proposal_path(us_id)
    
    if not os.path.exists(proposal_path):
        print(f"❌ No se encuentra la propuesta: {proposal_path}")
        return False
    
    print(f"\n{'='*60}")
    print(f"🚫 RECHAZANDO PROPUESTA: {us_id}")
    print(f"{'='*60}\n")
    
    # Motivo del rechazo
    reason = input("Motivo del rechazo (opcional): ")
    
    # Registrar rechazo
    log = load_applied_log()
    log[us_id] = {
        "rejected_at": datetime.now().isoformat(),
        "reason": reason,
        "status": "rejected"
    }
    save_applied_log(log)
    
    # Archivar propuesta
    archive_path = os.path.join(PROPOSALS_PATH, "rejected")
    os.makedirs(archive_path, exist_ok=True)
    rejected_proposal = os.path.join(archive_path, f"{us_id}_service_changes.md")
    shutil.move(proposal_path, rejected_proposal)
    
    print(f"\n✅ Propuesta rechazada y archivada")
    print(f"📁 Propuesta movida a: {rejected_proposal}")
    
    return True


def show_status(us_id):
    """Muestra el estado de una propuesta"""
    proposal_path = get_proposal_path(us_id)
    log = load_applied_log()
    
    print(f"\n{'='*60}")
    print(f"📊 ESTADO DE {us_id}")
    print(f"{'='*60}\n")
    
    if us_id in log:
        status = log[us_id]
        print(f"Estado: {status['status']}")
        if 'approved_at' in status:
            print(f"Aprobada: {status['approved_at']}")
        if 'rejected_at' in status:
            print(f"Rechazada: {status['rejected_at']}")
            print(f"Motivo: {status.get('reason', 'No especificado')}")
    elif os.path.exists(proposal_path):
        print("Estado: Pendiente de revisión")
        print(f"Propuesta disponible en: {proposal_path}")
    else:
        print("Estado: No encontrada")
    
    print()


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    
    us_id = sys.argv[1].upper()
    action = sys.argv[2].lower()
    
    if not us_id.startswith("US-"):
        print("❌ El ID debe tener formato US-XXX")
        sys.exit(1)
    
    if action == "--approve":
        approve_proposal(us_id)
    elif action == "--reject":
        reject_proposal(us_id)
    elif action == "--status":
        show_status(us_id)
    else:
        print(f"❌ Acción no válida: {action}")
        print("Usa: --approve, --reject, o --status")
        sys.exit(1)


if __name__ == "__main__":
    main()
