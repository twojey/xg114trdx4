using System;
using System.IO;
using System.Text;


namespace hello_world
{
    class ParseClass
    {
        KitchenPC.NLP.Parser parser;
        KitchenPC.Context.IKPCContext context;
        public ParseClass(KitchenPC.Context.IKPCContext context)
        {
            this.context = context;
            this.parser = context.Parser;
            this.parser.LoadTemplates("[ING]: [AMT] [UNIT]", //cheddar cheese: 5 cups
            "[AMT] [UNIT] [FORM] [ING]", //5 cups melted cheddar cheese
            "[AMT] [UNIT] [ING]", //5 cups cheddar cheese
            "[AMT] [UNIT] of [ING]", //5 cups of cheddar cheese
            "[AMT] [UNIT] of [FORM] [ING]", //two cups of shredded cheddar cheese
            "[AMT] [ING]", //5 eggs 
            "[ING]: [AMT]", //eggs: 5
            "[FORM] [ING]: [AMT]", //shredded cheddar cheese: 1 cup
            "[FORM] [ING]: [AMT] [UNIT]", //shredded cheddar cheese: 1 cup

            "[ING]: [AMT] [UNIT], [PREP]", //cheddar cheese: 5 cups
            "[AMT] [UNIT] [FORM] [ING], [PREP]", //5 cups melted cheddar cheese
            "[AMT] [UNIT] [ING], [PREP]", //5 cups cheddar cheese
            "[AMT] [UNIT] of [ING], [PREP]", //5 cups of cheddar cheese
            "[AMT] [UNIT] of [FORM] [ING], [PREP]", //two cups of shredded cheddar cheese
            "[AMT] [ING], [PREP]", //5 eggs
            "[ING]: [AMT], [PREP]", //eggs: 5
            "[FORM] [ING]: [AMT], [PREP]", //shredded cheddar cheese: 1 cup
            "[FORM] [ING]: [AMT] [UNIT], [PREP]", //shredded cheddar cheese: 1 cup
            "[ING] [AMT] [UNIT]",
            "[AMT] [AMT] [UNIT] [ING]"
            );
        }
        public void ParseUsageDoc(String filepathname, String poubellepathname, String recettename)
        {
            Console.WriteLine("On commence " + filepathname);
            var poubellestring = new StringBuilder();
            var recettestring = new StringBuilder();
            var cpt_match = 0;
            var cpt_nomatch = 0;
            var i = 0;


            using (StreamReader sr = new StreamReader(filepathname))
            {
                String line;

                while ((line = sr.ReadLine()) != null)
                {
                    string[] parts = line.Split(',');
                    if (i != 0) //Ne pas lire le Header
                    {
                        Console.WriteLine(parts[1]);
                        var result = this.context.ParseIngredientUsage(parts[1]);
                        if (i % 10000 == 0)
                        {
                            Console.WriteLine("Début du packet :" + i);
                        }
                        if (result.Status.ToString() == "NoMatch")
                        {
                            cpt_nomatch++;
                            var newLine = string.Format("{0},{1},{2}", parts[0], parts[1],result.Status.ToString());
                            poubellestring.AppendLine(newLine);

                        }
                        else
                        {
                            //Modifier Core/NLP/Result.cs pour avoir les ingrédients sur des matchs incomplets
                            if (result.Status.ToString() == "Match" || result.Status.ToString() == "PartialMatch")
                            {
                                cpt_match++;
                                var newLine = string.Format("{0};{1};{2}", parts[0], result.Usage.Ingredient.Name, result.Usage.Ingredient.Id);
                                recettestring.AppendLine(newLine);
                            }
                            else
                            {
                                cpt_nomatch++;
                                var newLine = string.Format("{0},{1}", parts[0], parts[1], result.Status.ToString());
                                poubellestring.AppendLine(newLine);
                            }


                        }

                    }
                    i = i + 1;
                }

            }
            Console.WriteLine("Match :" + cpt_match);
            Console.WriteLine("NoMatch :" + cpt_nomatch);
            File.WriteAllText(recettename, recettestring.ToString());
            File.WriteAllText(poubellepathname, poubellestring.ToString());


        }



    }
}