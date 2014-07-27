import nltk
import re
import json

nltk.download('maxent_ne_chunker')
nltk.download('maxent_treebank_pos_tagger')
nltk.download('punkt')
nltk.download('words')

def do_ner(text):
	print text
	rl = []
	np = []
	ne = []
        for sentence in nltk.sent_tokenize(text): #re.sub(r'[^\x00-\x7F]+',' ', text)):

            sentence_tok = nltk.word_tokenize(sentence)
            sentence_tok = nltk.pos_tag(sentence_tok)


	    grammar = r"""
  NP: {<DT|PP\$>?<JJ|JJR|JJS>*<NN|NNP|NNS|NNPS>+}   # chunk adjectives and noun
""" #      {<NNP>+}                # chunk sequences of proper nouns
#"""        
            cp = nltk.RegexpParser(grammar)

	    ret = dict()
            ret['sentence'] = sentence
            ret['npr'] = cp.parse(sentence_tok)
            ret['ner'] = nltk.ne_chunk(sentence_tok, binary=True)
	    ret['noun_phrases_tree'] = filter(lambda x: x.node == 'NP', ret['npr'].subtrees())
	    ret['named_entities_tree'] = filter(lambda x: x.node == 'NE', ret['ner'].subtrees())
	    np += [" ".join(w[0] for w in t.leaves()) for t in ret['noun_phrases_tree']]
	    ne += [" ".join(w[0] for w in t.leaves()) for t in ret['named_entities_tree']]
	    rl.append(ret)
	ne_sort = list(set(ne))
	np_sort = list(set(np))
	ne_sort.sort(key=len, reverse=True)
	np_sort.sort(key=len, reverse=True)
	np_filter = filter(lambda x: len(x) >= 15, np_sort)
	best_guess = []
	best_guess += ne_sort[:10]
	if len(ne_sort) == 0:
		best_guess += np_filter[:10]
	else:
		best_guess += np_filter[:5]
	if len(best_guess) == 0:
		best_guess += np_sort
	return json.dumps({'noun_phrases': np, 'named_entities': ne, 'best_guess':best_guess}, sort_keys=True, indent=4, separators=(',',': '))


if __name__ == "__main__":

    sentence = "12 dogs with controversial opinions about the sanitary conditions on the BART"

    sentence = "The Washington Monument is the most prominent structure in Washington, D.C. and one of the city's early attractions. It was built in honor of George Washington, who led the country to independence and then became its first President."

    text = '''

29 Essentials For Throwing The Perfect "Harry Potter" Party

1. Send out owl balloon party invitations.
Send out owl balloon party invitations.

Use owl balloons to deliver your party invitations door-to-door. Create your own Hedwig balloon using these instructions to get people excited to attend your Harry Potter smash.
2. Recreate the entrance to platform 9 3/4 for Hogwarts Express.
Recreate the entrance to platform 9 3/4 for Hogwarts Express.

Make your own secret route to Hogwarts Express using these instructions.
3. Set up floating candles in your own version of the Great Hall.
Set up floating candles in your own version of the Great Hall.
encyclopediahomeschoolica.com

Create the *spooky* setting in your house using these instructions here.
4. Make a photo booth for guests to pose as escaped wizards from Azkaban.
Make a photo booth for guests to pose as escaped wizards from Azkaban.
funfilledflicks.com

Everyone can feel like Sirius Black for a day using foam and a little ingenuity.
5. Create Gryffindor ties for everyone to wear.
Create Gryffindor ties for everyone to wear.
parenting.com

You can download and print the ties here and then ta-da  you are a Gryffindor as far as anyone knows!
6. Arrange a quidditch pitch on your lawn.
Arrange a quidditch pitch on your lawn.
blog.hwtm.com

Guests can understand what it feels like to pursue the snitch for a day. Make your own using this example.
7. Place potion jars as a centerpiece just like those found in Snapes cabinet.
Place potion jars as a centerpiece just like those found in Snape's cabinet.
squidoo.com

Learn how to make them look exactly like the real thing here.
8. Make or buy your own sorting hat to place everyone in houses.
Make or buy your own sorting hat to place everyone in houses.
thinkgeek.com

You can buy it or make one using paper mch and newspaper using these instructions.
9. Use your old Flourish and Blotts textbooks as a cake stand.
Use your old Flourish and Blotts' textbooks as a cake stand.
centsationalgirl.com

Make your own DIY textbooks exactly like the books in the films here.
10. Hang school banners from every house to spruce up the party.
Hang school banners from every house to spruce up the party.
centsationalgirl.com

Announce your loyalties to the different houses by hanging these banners. Create your own banners using the instructions here.
11. Post directions to every fictional spot in the novels.
Post directions to every fictional spot in the novels.
centsationalgirl.com

Assemble your own directions using this DIY guide.
Thinkstock
12. Throw on a cape and round glasses to become Harry Potter, the Chosen One.
instagram.com

Become the one and only Harry with these instructions.
13. Dress up like the red-haired and wand-wielding wizard, Ron Weasley.
Dress up like the red-haired and wand-wielding wizard, Ron Weasley.
cosplaycollector.com

Embrace the sidekick in you using these instructions here.
14. Embrace your inner smartypants and throw on this costume to become Hermione Granger.
Embrace your inner smartypants and throw on this costume to become Hermione Granger.
cosgeek.blogspot.com

Find out how to become the noble and knowledgeable Hermione here.
15. You will be the most talked-about guest at your party if you dress up like Moaning Myrtle.
You will be the most "talked-about" guest at your party if you dress up like Moaning Myrtle.
dearthduo.blogspot.com

You, too, can haunt the bathroom like Myrtle does in the book using this guide here.
16. Put on some glasses and hold a crystal ball to be the Professor Trelawney of your party.
Put on some glasses and hold a crystal ball to be the Professor Trelawney of your party.
fromdahliastodoxies.blogspot.com

Create your own papier-mch hair and your own crystal ball just like the professor using these instructions.
17. Win the costume contest with this special Mad Eye Moody costume.
instagram.com

Create your own DIY verision using this guide here.
Thinkstock
18. Impress your friends with some butterbeer, just like the one served at The Three Broomsticks in Hogsmeade.
Impress your friends with some butterbeer, just like the one served at The Three Broomsticks in Hogsmeade.
cupcakediariesblog.com

Create your own version of this Diagon Alley drink using this recipe here.
19. Spruce up your pong game with the ultimate round of quidditch pong.
Spruce up your pong game with the ultimate round of quidditch pong.
foodbeast.com

Make your own quidditch hoops using ducktape from this guide here.
20. Class up the party with a Golden Snitch cocktail.
Class up the party with a "Golden Snitch" cocktail.
sashahalima.com

Use this recipe to create your own version of this cocktail.
21. Blow everyone away with this goblet of FIRE cocktail.
Blow everyone away with this goblet of FIRE cocktail.
sashahalima.com

Learn how to make this special elixir here.
22. Upgrade party drinks easily by adding food coloring.
Upgrade party drinks easily by adding food coloring.
blog.hwtm.com

See how to make your own version here.
23. Detail each cocktail with cute little broomsticks.
Detail each cocktail with cute little broomsticks.
cakeeventsblog.com

Add a little spice to your butterbeer by making cute broomsticks for each drink. Check out how to make them using raffia here.
Thinkstock
24. Instead of cupcakes, serve everyone Cauldron cakes with gold frosting.
Instead of cupcakes, serve everyone Cauldron cakes with gold frosting.
blog.booturtle.com

Make your own version of these cauldron cakes using this recipe here.
25. Make everyone feel like they are living out their book dreams by serving Acid pops.
Make everyone feel like they are living out their book dreams by serving Acid pops.
blog.booturtle.com

Make your own just like the ones Harry had in Honeydukes Sweetshop in Hogsmeade! This recipe uses pop rocks and tootsie pops.
26. Create Golden Snitch Cake Pops with wings.
Create Golden Snitch Cake Pops with wings.
centsationalgirl.com

Make your own with this recipe here.
27. Serve licorice wands just like the ones on the food trolley on Hogwarts Express.
Serve licorice wands just like the ones on the food trolley on Hogwarts Express.
pastryaffair.com

28. Even if the real characters arent at the party, you can at least make sugar cookies of your favorite ones.
Even if the real characters aren't at the party, you can at least make sugar cookies of your favorite ones.

29. Chocolate frogs are the most iconic snack from the book, and you can easily make them for your party.
Chocolate frogs are the most iconic snack from the book, and you can easily make them for your party.

Create your own just like the ones Harry gets on the Hogwarts Express using chocolate mold via this guide.
Dont forget to bust out your muggle moves on everyone at the party.
'''

    for sentence in nltk.sent_tokenize(text): #re.sub(r'[^\x00-\x7F]+',' ', text)):

        sentence_tok = nltk.word_tokenize(sentence)
        sentence_tok = nltk.pos_tag(sentence_tok)
        
        grammar = "NP: {<DT>?<JJ>*<NN>}"
        cp = nltk.RegexpParser(grammar)

        print sentence
        print cp.parse(sentence_tok)
        print nltk.ne_chunk(sentence_tok)
