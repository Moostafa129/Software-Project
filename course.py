from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Course(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    
    # Add relationship to students
    students: Mapped[list["Student"]] = relationship(
        secondary="student_course",
        back_populates="courses"
    )
    
    # Add relationship to grades
    grades: Mapped[list["Grade"]] = relationship(back_populates="course")
