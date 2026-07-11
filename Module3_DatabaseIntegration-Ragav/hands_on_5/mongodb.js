// TASK 1 : CREATE COLLECTION

// use college_nosql
db.createCollection("feedback");

db.feedback.insertMany([
  {
    student_id: 1,
    course_code: "CS101",
    semester: "2022-ODD",
    rating: 5,
    comments: "Excellent teaching.",
    tags: ["challenging", "well-structured", "good-examples"],
    submitted_at: ISODate("2022-11-30T10:15:00Z"),
    attachments: [{ filename: "notes.pdf", size_kb: 240 }],
  },
  {
    student_id: 2,
    course_code: "CS101",
    semester: "2022-ODD",
    rating: 4,
    comments: "Very informative.",
    tags: ["challenging", "practical"],
    submitted_at: ISODate("2022-11-29T09:00:00Z"),
    attachments: [{ filename: "assignment.pdf", size_kb: 120 }],
  },
  {
    student_id: 3,
    course_code: "CS101",
    semester: "2022-EVEN",
    rating: 2,
    comments: "Too difficult.",
    tags: ["challenging", "fast-paced"],
    submitted_at: ISODate("2022-06-15T12:00:00Z"),
  },
  {
    student_id: 4,
    course_code: "CS102",
    semester: "2022-ODD",
    rating: 5,
    comments: "Loved the labs.",
    tags: ["hands-on", "interesting"],
    submitted_at: ISODate("2022-11-20T08:00:00Z"),
    attachments: [{ filename: "labwork.pdf", size_kb: 180 }],
  },
  {
    student_id: 5,
    course_code: "CS102",
    semester: "2022-EVEN",
    rating: 3,
    comments: "Average experience.",
    tags: ["theory", "moderate"],
    submitted_at: ISODate("2022-05-20T10:00:00Z"),
    attachments: [{ filename: "notes.docx", size_kb: 80 }],
  },
  {
    student_id: 6,
    course_code: "CS103",
    semester: "2022-ODD",
    rating: 5,
    comments: "Excellent examples.",
    tags: ["good-examples", "interactive"],
    submitted_at: ISODate("2022-11-25T15:00:00Z"),
    attachments: [{ filename: "slides.pdf", size_kb: 350 }],
  },
  {
    student_id: 7,
    course_code: "CS103",
    semester: "2021-EVEN",
    rating: 1,
    comments: "Poorly organized.",
    tags: ["confusing"],
    submitted_at: ISODate("2021-12-10T14:00:00Z"),
    attachments: [{ filename: "review.txt", size_kb: 20 }],
  },
  {
    student_id: 8,
    course_code: "CS104",
    semester: "2022-ODD",
    rating: 4,
    comments: "Good overall.",
    tags: ["well-structured"],
    submitted_at: ISODate("2022-11-10T11:00:00Z"),
    attachments: [{ filename: "summary.pdf", size_kb: 140 }],
  },
  {
    student_id: 9,
    course_code: "CS104",
    semester: "2021-EVEN",
    rating: 2,
    comments: "Needs improvement.",
    tags: ["confusing", "boring"],
    submitted_at: ISODate("2021-11-18T10:30:00Z"),
    attachments: [{ filename: "feedback.doc", size_kb: 60 }],
  },
  {
    student_id: 10,
    course_code: "CS105",
    semester: "2022-ODD",
    rating: 5,
    comments: "Outstanding course.",
    tags: ["excellent", "challenging"],
    submitted_at: ISODate("2022-11-28T09:30:00Z"),
    attachments: [{ filename: "project.zip", size_kb: 500 }],
  },
]);

db.feedback.countDocuments();

// TASK 2: CRUD OPERATIONS
//
db.feedback.find({
  rating: 5,
});

db.feedback.find({
  course_code: "CS101",
  tags: "challenging",
});

db.feedback.find(
  {},
  {
    student_id: 1,
    course_code: 1,
    rating: 1,
    _id: 0,
  },
);

db.feedback.updateMany(
  {
    rating: { $lt: 3 },
  },
  {
    $set: {
      needs_review: true,
    },
  },
);

db.feedback.updateMany(
  {
    needs_review: true,
  },
  {
    $push: {
      tags: "reviewed",
    },
  },
);

db.feedback.deleteMany({
  semester: "2021-EVEN",
});

// TASK 3: AGGREGATION PIPELINE

db.feedback.aggregate([
  {
    $match: {
      semester: "2022-ODD",
    },
  },
  {
    $group: {
      _id: "$course_code",
      avg_rating: {
        $avg: "$rating",
      },
      total_feedback: {
        $sum: 1,
      },
    },
  },
  {
    $sort: {
      avg_rating: -1,
    },
  },
]);

db.feedback.aggregate([
  {
    $match: {
      semester: "2022-ODD",
    },
  },
  {
    $group: {
      _id: "$course_code",
      avg_rating: {
        $avg: "$rating",
      },
      total_feedback: {
        $sum: 1,
      },
    },
  },
  {
    $project: {
      _id: 0,
      course_code: "$_id",
      average_rating: {
        $round: ["$avg_rating", 1],
      },
      total_feedback: 1,
    },
  },
  {
    $sort: {
      average_rating: -1,
    },
  },
]);

db.feedback.aggregate([
  {
    $unwind: "$tags",
  },
  {
    $group: {
      _id: "$tags",
      count: {
        $sum: 1,
      },
    },
  },
  {
    $sort: {
      count: -1,
    },
  },
]);

db.feedback.createIndex({
  course_code: 1,
});
