# Why swagger v2 instead on 3

I found that the library we are using (aka flakon) only supports the parsing of swagger v2. So I downgraded our model with using [this tool](https://lucybot-inc.github.io/api-spec-converter/).

# Why forked flakon
 
I found that the library we are using (aka flakon) does not support the 'parameters' property in the api definitions. So I created a simple fork with [few changes](https://github.com/Runnerly/flakon/compare/master...giacomodeliberali:master) and I updated the requirements.txt with this new fork in order to make travis properly work.
