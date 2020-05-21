import unittest
import user as u
import resource as r
import server as s
import socket, errno
import hasher
class Tester(unittest.TestCase):

    #User tests
    #------------------------------------------------
    #Tests if new user has a correct data
    #id:0, username:"Kowalski", passwordhash:"abcdef"
    def testRegisterNewUserCorrectData(self):
        testuser = u.User.registerNewUser(0,"Kowalski","abcdef")
        self.assertEqual("Kowalski", testuser.getUsername()) #Correct username
        self.assertEqual(hasher.hash(str(0)+"Kowalski"+"abcdef"), testuser.getAuthCode()) #Generating correct authCode
        self.assertEqual(0, testuser.getTotalPoints()) #Starting points == 0

    #Tests user equality
    def testUserEqual(self):
        testuser1 = u.User.registerNewUser(3,"Joseph","eee")
        testuser2 = u.User.registerNewUser(3,"Joseph","eee")
        self.assertEqual(testuser1,testuser2)

    #Tests JSON saving/loading
    #ensures that saved user will always be loaded correctly
    def testJSONSaving(self):
        testuser = u.User.registerNewUser(10,"Jordan","123def")
        testuserloaded = u.User.loadFromJSON(testuser.serialize())
        self.assertEqual(testuser,testuserloaded)

        testuser1 = u.User.registerNewUser(12,"Adam","000999aa")
        testuserloaded1 = u.User.loadFromJSON(testuser1.serialize())
        self.assertEqual(testuser1,testuserloaded1)

        #Test of same data, different ids, even though it would be incorrect to make two users with same username
        testuser3 = u.User.registerNewUser(4,"Jon","eee")
        testuser4 = u.User.registerNewUser(5,"Jon","eee")
        self.assertEqual(False,testuser3==testuser4)

    #Tests if adding points works
    def testUserPointAddition(self):
        testuser = u.User.registerNewUser(0,"Kowalski","abcdef")
        testuser.addPointsForResource("http://127.0.0.1:5000/wiki?title=France", 50, 100)
        self.assertEqual(50, testuser.getResourcePointsForResource("http://127.0.0.1:5000/wiki?title=France")[0])
        self.assertEqual(100, testuser.getResourcePointsForResource("http://127.0.0.1:5000/wiki?title=France")[1])

        testuser.addPointsForResource("http://127.0.0.1:5000/wiki?title=Poland", 75, 200)
        self.assertEqual(75, testuser.getResourcePointsForResource("http://127.0.0.1:5000/wiki?title=Poland")[0])
        self.assertEqual(200, testuser.getResourcePointsForResource("http://127.0.0.1:5000/wiki?title=Poland")[1])

        testuser.addPointsForResource("http://127.0.0.1:5000/wiki?title=Poland", 50, 200)
        self.assertEqual(125, testuser.getResourcePointsForResource("http://127.0.0.1:5000/wiki?title=Poland")[0])
        self.assertEqual(200, testuser.getResourcePointsForResource("http://127.0.0.1:5000/wiki?title=Poland")[1])

        testuser.addPointsForResource("http://127.0.0.1:5000/wiki?title=Poland", 100, 200)
        self.assertEqual(200, testuser.getResourcePointsForResource("http://127.0.0.1:5000/wiki?title=Poland")[0])
        self.assertEqual(200, testuser.getResourcePointsForResource("http://127.0.0.1:5000/wiki?title=Poland")[1])

        self.assertRaises(KeyError, lambda: testuser.getResourcePointsDict()["other-entry"])
    
    
    #Resource tests
    #------------------------------------------------
    #Inits and gets
    def testResourceInit(self):
        res1 = r.Resource("http://127.0.0.1:5000/wiki?title=Poland", 32)
        self.assertEqual("http://127.0.0.1:5000/wiki?title=Poland", res1.getLink())
        self.assertEqual(32, res1.getCategoryID())
        self.assertEqual(100, res1.getMaxPoints()) #Resources base maxpoints is 100
        self.assertEqual([], res1.getComments())
        

    def testWikipediaInit(self):
        #trying to make a resource from wikipedia that doesnt exist
        self.assertRaises(AssertionError, lambda: r.WikipediaResource("thisAAArticleDOESNTexist!!",0))

        res2 = r.WikipediaResource("http://127.0.0.1:5000/wiki?title=France")
        self.assertEqual("http://127.0.0.1:5000/wiki?title=France", res2.getLink())
        self.assertEqual(1, res2.getCategoryID()) #wikipedia articles are always category 1
        self.assertGreaterEqual(res2.getMaxPoints(), 100) 
        #max points are calculated accordingly to their length, may vary over time, but always more than or equal 100

        res3 = r.WikipediaResource("http://127.0.0.1:5000/wiki?title=Poland", 4)
        self.assertEqual(4, res3.getCategoryID()) #wikipedia articles are always category 1 unless we tell them to be other
    
    def testPolonaInit(self):
        self.assertRaises(AssertionError, lambda: r.PolonaResource("www.wronglink.com"))

        res1 = r.PolonaResource("http://127.0.0.1:5000/polona?title=dziela-wiliama-szekspira-t-9-komedye&page=0")

        self.assertEqual("http://127.0.0.1:5000/polona?title=dziela-wiliama-szekspira-t-9-komedye", res1.getLink())
        self.assertEqual(2, res1.getCategoryID()) #polona articles are always category 2
        self.assertEqual(4960, res1.getMaxPoints()) #max points limit for polona books is equal to number of scans * 10 and this book has 147 scans

    def testRecalculateMaxPoints(self):
        res1 = r.Resource("link-to-some-resource", 22)
        res1.recalculateMaxPoints()
        self.assertEqual(100, res1.getMaxPoints()) #base resources will always have their maxpoints recalculated to 100

        #wikipedia resources have max points relative to their length, so in this moment
        #any wikipedia resource should have the same length and thus maxpoints
        res2 = r.WikipediaResource("http://127.0.0.1:5000/wiki?title=Charlemagne")
        pointspre = res2.getMaxPoints()
        res2.recalculateMaxPoints()
        self.assertEqual(pointspre, res2.getMaxPoints()) 

        res3 = r.PolonaResource("http://127.0.0.1:5000/polona?title=dziela-wiliama-szekspira-t-9-komedye&page=0")
        pointspre = res3.getMaxPoints()
        res3.recalculateMaxPoints()
        self.assertEqual(pointspre, res3.getMaxPoints())

    #Since sub-classes don't change how comments are added/removed, we use base class
    def testCommentAdding(self):
        res3 = r.Resource("link-to-resource",0)
        res3.addComment(0,2,"Nice, thanks!")
        self.assertEqual([r.Comment(0,2,"Nice, thanks!")], res3.getComments())
        res3.addComment(1,3,"Lorem ipsum")
        self.assertEqual([r.Comment(0,2,"Nice, thanks!"), r.Comment(1,3,"Lorem ipsum")], res3.getComments())

    #Prevent comment duplicate
    def testCommentAddingDuplicate(self):
        res3 = r.Resource("link-to-resource",0)
        res3.addComment(0,2,"Nice, thanks!")
        self.assertEqual([r.Comment(0,2,"Nice, thanks!")], res3.getComments())
        res3.addComment(1,2,"Nice, thanks!")
        self.assertEqual([r.Comment(0,2,"Nice, thanks!")], res3.getComments())

    def testCommentRemoving(self):
        res3 = r.Resource("link-to-resource",0)
        res3.addComment(0,2,"Nice, thanks!")
        res3.addComment(1,3,"Lorem ipsum")
        res3.removeComment(0)
        self.assertEqual([r.Comment(1,3,"Lorem ipsum")], res3.getComments())
        res3.removeComment(1)
        self.assertEqual([], res3.getComments())
        res3.removeComment(-231)
        self.assertEqual([], res3.getComments())

    #Server tests
    #--------------------------------
    #Check if initialization and running is correct
    def testServerRunning(self):
        server = s.Server("127.0.0.1", 5000)
        server.runServer()

        self.assertTrue(server.running())
        self.assertEqual("127.0.0.1", server.ip)
        self.assertEqual(5000, server.port)

    #calculates number of all players
    def testTotalUsers(self):
        server = s.Server("127.0.0.1", 5000)
        server.registerNewUser("user1","passwordhash1")
        self.assertEqual(1, server.totalUserCount())

        server.registerNewUser("user1","passwordhash2") #user already exists, dont register him
        self.assertEqual(1, server.totalUserCount())

        server.registerNewUser("user2","passwordhash1")
        self.assertEqual(2, server.totalUserCount())

        server.registerNewUser("user3","passwordhash3")
        server.registerNewUser("user4","passwordhash4")

        self.assertEqual(4, server.totalUserCount())

        server.registerNewUser("user3","passwordhash3")#user already exists, dont register him
        server.registerNewUser("user4","passwordhash4")#user already exists, dont register him

        self.assertEqual(4, server.totalUserCount())

    def testRegisterUserID(self):
        server = s.Server("127.0.0.1", 5000)
        uid = server.registerNewUser("user1","passwordhash1")
        self.assertEqual(0, uid)

        uid = server.registerNewUser("user1","passwordhash1") #user already exists, return its id
        self.assertEqual(0, uid)

        uid = server.registerNewUser("user2","passwordhash2") 
        self.assertEqual(1, uid)

        uid = server.registerNewUser("user3","passwordhash3") 
        self.assertEqual(2, uid)

        uid = server.registerNewUser("user2","passwordhash4") #user already exists, return its id
        self.assertEqual(1, uid)

    #Saved user in server == user created with User.registerNewUser
    def testRegisterUserData(self):
        server = s.Server("127.0.0.1", 5000)
        uid = server.registerNewUser("testuser","testpassword")
        user =  u.User.registerNewUser(0,"testuser","testpassword")
        self.assertEqual(server.getUser(uid), user)


    def testAddPointsForBrowsing(self):
        server = s.Server("127.0.0.1", 5000)

        uid = server.registerNewUser("user1","passwordhash1")

        #each minute browsing = 15 points
        #from earlier test we know that this resource will be maximally worth 4960 points
        self.assertEqual(150, server.addPointsForUser(uid, server.getUser(uid).getAuthCode(),"http://127.0.0.1:5000/polona?title=dziela-wiliama-szekspira-t-9-komedye&page=0", 10.0)[0])
        #dont accept negative or 0 time or when authcode is incorrect
        self.assertEqual(150, server.addPointsForUser(uid, server.getUser(uid).getAuthCode(),"http://127.0.0.1:5000/polona?title=dziela-wiliama-szekspira-t-9-komedye&page=0", -30.0)[0])
        self.assertEqual(150, server.addPointsForUser(uid, server.getUser(uid).getAuthCode(),"http://127.0.0.1:5000/polona?title=dziela-wiliama-szekspira-t-9-komedye&page=0", 0.0)[0])
        self.assertEqual(150, server.addPointsForUser(uid, 1,"http://127.0.0.1:5000/polona?title=dziela-wiliama-szekspira-t-9-komedye&page=0", 0.0)[0])

        self.assertEqual(300, server.addPointsForUser(uid, server.getUser(uid).getAuthCode(),"http://127.0.0.1:5000/polona?title=dziela-wiliama-szekspira-t-9-komedye&page=0", 10.0)[0])
        self.assertEqual(675, server.addPointsForUser(uid, server.getUser(uid).getAuthCode(),"http://127.0.0.1:5000/polona?title=dziela-wiliama-szekspira-t-9-komedye&page=0", 25.0)[0])
        self.assertEqual(4960, server.addPointsForUser(uid, server.getUser(uid).getAuthCode(),"http://127.0.0.1:5000/polona?title=dziela-wiliama-szekspira-t-9-komedye&page=0", 5000.0)[0])

    #show the most popular resource in each category that has the highest number of unique visits
    def testRecommendedResource(self):
        server = s.Server("127.0.0.1", 5000)
        uid = server.registerNewUser("user1","passwordhash1")

        server.addPointsForUser(uid, server.getUser(uid).getAuthCode(),"http://127.0.0.1:5000/polona?title=dziela-wiliama-szekspira-t-9-komedye&page=0", 10.0)
        server.addPointsForUser(uid, server.getUser(uid).getAuthCode(),"http://127.0.0.1:5000/polona?title=dziela-wiliama-szekspira-t-9-komedye&page=0", 10.0)
        server.addPointsForUser(uid, server.getUser(uid).getAuthCode(),"http://127.0.0.1:5000/polona?title=karpaty-i-podkarpacie&page=0", 10.0)

        uid = server.registerNewUser("user2","passwordhash2")
        server.addPointsForUser(uid, server.getUser(uid).getAuthCode(),"http://127.0.0.1:5000/polona?title=pisma-adama-mickiewicza-t-5&page=0", 10.0)
        server.addPointsForUser(uid, server.getUser(uid).getAuthCode(),"http://127.0.0.1:5000/polona?title=dziela-wiliama-szekspira-t-9-komedye&page=0", 10.0)

        uid = server.registerNewUser("user3","passwordhash3")
        server.addPointsForUser(uid, server.getUser(uid).getAuthCode(),"http://127.0.0.1:5000/polona?title=dziela-wiliama-szekspira-t-9-komedye&page=0", 10.0)
        server.addPointsForUser(uid, server.getUser(uid).getAuthCode(),"http://127.0.0.1:5000/polona?title=karpaty-i-podkarpacie&page=0", 10.0)

        server.rdb.createRanking(2,False)
        self.assertEqual([["http://127.0.0.1:5000/polona?title=dziela-wiliama-szekspira-t-9-komedye","dziela-wiliama-szekspira-t-9-komedye",3]], server.recommendFromCat(0,2,1))
        self.assertEqual([["http://127.0.0.1:5000/polona?title=karpaty-i-podkarpacie","karpaty-i-podkarpacie",2]], server.recommendFromCat(1,2,1))
        self.assertEqual([["http://127.0.0.1:5000/polona?title=pisma-adama-mickiewicza-t-5","pisma-adama-mickiewicza-t-5",1]], server.recommendFromCat(2,2,1))
        self.assertEqual([["","",0]], server.recommendFromCat(3,2,1))

        self.assertEqual([
        ["http://127.0.0.1:5000/polona?title=dziela-wiliama-szekspira-t-9-komedye","dziela-wiliama-szekspira-t-9-komedye",3],
        ["http://127.0.0.1:5000/polona?title=karpaty-i-podkarpacie","karpaty-i-podkarpacie",2],
        ["http://127.0.0.1:5000/polona?title=pisma-adama-mickiewicza-t-5","pisma-adama-mickiewicza-t-5",1]], server.recommendFromCat(0,2,3))

        server.rdb.createRanking(1,False)
        self.assertEqual([["","",0]], server.recommendFromCat(0,1,1)) #no wikipedia article has beed read

        server.addPointsForUser(uid, server.getUser(uid).getAuthCode(),"http://127.0.0.1:5000/wiki?title=Benjamin_Netanyahu", 10.0)

        server.rdb.createRanking(1,False)
        self.assertEqual([["http://127.0.0.1:5000/wiki?title=Benjamin_Netanyahu","Benjamin_Netanyahu",1]], server.recommendFromCat(0,1,1)) 
        self.assertEqual([["","",0]], server.recommendFromCat(1,1,1)) 

        server.addPointsForUser(uid, server.getUser(uid).getAuthCode(),"http://127.0.0.1:5000/wiki?title=Colorado", 10.0)

        server.rdb.createRanking(1,False)
        self.assertEqual([["http://127.0.0.1:5000/wiki?title=Benjamin_Netanyahu","Benjamin_Netanyahu",1]], server.recommendFromCat(0,1,1)) 
        self.assertEqual([["http://127.0.0.1:5000/wiki?title=Colorado","Colorado",1]], server.recommendFromCat(1,1,1)) 
        self.assertEqual([["","",0]], server.recommendFromCat(2,1,1)) 

        server.resetServer()

    
if( __name__ == '__main__'):
    unittest.main()