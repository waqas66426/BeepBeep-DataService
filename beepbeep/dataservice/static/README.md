
# Unofficial API

the user credentials should be detached from the table user in the micro service db

/user
  PUT to create the user (return the id?)

  /user/<id>
    GET the user by id
    DELETE to delete the user by id (it will delete on cascade the other table fields related to that user)

  /user/byemail/<email@email.com>
    GET the user by email


/runs

  /runs/maxrunid
    GET like doing a select max(id) query on the db

  /runs/<runner_id>?number=<number_of_runs>
   GET to ge the run by user id (already implemented)


/objectvie 
  PUT to create the objective (return the id?)

  /objective/<runner_id>
    GET get the objectvie by user id
    POST to set the new objective


/challenge
  PUT to create a challenge

  /challenge/<runner_id>
    GET to get the challenge by user id
    DELETE to delete the challenge before challenging anathor one
