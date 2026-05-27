from typing import Dict, Any, Optional
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import GraphNode
from app.services.registry import TargetRegistryService

async def get_or_create_node(session: AsyncSession, node_type: str, name: str, sector: Optional[str] = None, attributes: Dict[str, Any] = None) -> GraphNode:
    result = await session.execute(
        select(GraphNode).where(GraphNode.node_type == node_type, GraphNode.name == name)
    )
    node = result.scalars().first()
    
    if not node:
        node = GraphNode(
            node_type=node_type,
            name=name,
            sector=sector,
            attributes=attributes or {}
        )
        session.add(node)
        await session.commit()
        await session.refresh(node)
        
    return node

async def ensure_company_node(session: AsyncSession, company_name: str) -> GraphNode:
    # Look up sector from registry if possible
    metadata = TargetRegistryService.get_all_targets().get(company_name, {})
    sector = metadata.get("sector", "Unknown")
    
    return await get_or_create_node(
        session=session,
        node_type="Company",
        name=company_name,
        sector=sector,
        attributes={"source": "auto_discovery"}
    )
