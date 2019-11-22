using System;
using KitchenPC.Context;
using KitchenPC;
using System.IO;
using System.Text;
using Microsoft.VisualBasic;

namespace hello_world
{
    class Program2
    {
        static void setup(string[] args)
        {
            Console.WriteLine("Hello Setup!");
            // Context connected to local data store
            var staticConfig = Configuration<StaticContext>.Build
               .Context(StaticContext.Configure
                  .DataDirectory(@"C:\Users\Moi\source\repos\core\src\SampleData")
                  .Identity(() => new AuthIdentity(new Guid("c52a2874-bf95-4b50-9d45-a85a84309e75"), "Mike"))
               )
               .Create();
            KPCContext.Initialize(staticConfig);
            var context = KPCContext.Current;
            var esult = context.ParseIngredient("1 tablespoon chopped coriander leaves");
            Console.WriteLine(esult);
            var zesult = context.ParseIngredientUsage("1 tablespoon chopped coriander leaves");
            Console.WriteLine(zesult.Usage);
            Console.WriteLine("CSV part");
            var path = "C:/Users/Moi/Downloads/Poubelle_3.csv";

            var poubellestring = new StringBuilder();
            var recettestring = new StringBuilder();
            var cpt_match = 0;
            var cpt_nomatch = 0;
            var i = 0;

            var parser = new KitchenPC.NLP.Parser();
            parser.LoadTemplates(
               "[ING]: [AMT] [UNIT]", //cheddar cheese: 5 cups
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
               "[FORM] [ING]: [AMT] [UNIT], [PREP]" //shredded cheddar cheese: 1 cup
               );
            var aesult = parser.Parse("banana");
            //Console.WriteLine(aesult.Usage.Ingredient.Name);

            using (StreamReader sr = new StreamReader(path))
            {
                String line;

                while ((line = sr.ReadLine()) != null)
                {
                    string[] parts = line.Split(',');

                    //string orderId = parts[2];
                    // Do what you need with the orderID
                    if (i != 0)
                    {
                        //Console.WriteLine(parts[1]);
                        var result = context.ParseIngredientUsage(parts[1]);

                        if (result.Status.ToString() == "NoMatch")
                        {
                            cpt_nomatch++;
                            //Console.WriteLine(result);
                            //Console.WriteLine(parts[1]);
                            var newLine = string.Format("{0},{1}", parts[0], parts[1]);
                            poubellestring.AppendLine(newLine);

                        }
                        else
                        {
                            //Modifier Core/NLP/Result.cs pour avoir les ingrédients sur des matchs incomplets
                            Console.WriteLine(result.Status);

                            cpt_match++;
                            var newLine = string.Format("{0},{1},{2}", parts[0], result.Usage.Ingredient.Name, result.Usage.Ingredient.Id);
                            recettestring.AppendLine(newLine);


                        }

                    }
                    i = i + 1;
                }

            }
            Console.WriteLine("Match :" + cpt_match);
            Console.WriteLine("NoMatch :" + cpt_nomatch);
            File.WriteAllText("C:/Users/Moi/Downloads/RECYCLAGE3.csv", recettestring.ToString());
            File.WriteAllText("C:/Users/Moi/Downloads/POUBELLE_FINALE3.csv", poubellestring.ToString());

        }
    }
}
