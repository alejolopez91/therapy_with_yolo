from db.database_manager import DatabaseManager
from repositories.joint_repository import JointRepository
from models.joint import Joint

def main():
    # Initialize
    db_manager = DatabaseManager()
    joint_repo = JointRepository(db_manager)

    # Create joints
    right_shoulder = Joint(
        name="RIGHT_SHOULDER",
        points=[8, 6, 5]
    )
    left_shoulder = Joint(
        name="LEFT_SHOULDER",
        points=[6, 5, 7]
    )
    saved_joint = joint_repo.create(right_shoulder)
    saved_joint2 = joint_repo.create(left_shoulder)

    # Get joint
    joint = joint_repo.get(saved_joint.id)
    print(f"Joint: {joint}")

if __name__ == "__main__":
    main()

# To run: PYTHONPATH=$PYTHONPATH:. python3 db/seeds/joint_seeds.py