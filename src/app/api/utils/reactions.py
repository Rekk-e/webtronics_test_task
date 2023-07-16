import json
from datetime import datetime
from typing import List

from app import repo

from app.api.schemas import Reaction


def deserialize(data, model) -> List[dict]:
    """
    function converts data from JSON format to a list of model instances
    """
    result = list()
    data = json.loads(data)
    for row in data:
        row["created_at"] = datetime.strptime(row["created_at"].split()[0], '%Y-%m-%d').date()
        result.append(model(**row))

    return result


def serialize(data) -> json:
    """
    The function converts the passed data to JSON format
    """
    result = list()
    for row in data:
        result.append({c.name: str(getattr(row, c.name)) for c in row.__table__.columns})
    if result:
        return json.dumps(result, indent=4, sort_keys=True, default=str)

    return None

async def get_reactions(post_id: int) -> List[Reaction]:
    """
    The function allows you to get all the reactions to the specified post
    """
    reactions = await repo.reaction.get_by_post(post_id)

    reaction_models = list()
    for reaction in reactions:
        reaction_model = Reaction(
            author_id=reaction.author_id,
            reaction=reaction.reaction,
            created_at=reaction.created_at
        )
        reaction_models.append(reaction_model)

    return reaction_models