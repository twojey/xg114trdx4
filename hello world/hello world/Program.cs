using System;
using KitchenPC.Context;
using KitchenPC;
using System.IO;
using System.Text;
using Microsoft.VisualBasic;

namespace hello_world
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello World!");
            // Context connected to local data store
            var staticConfig = Configuration<StaticContext>.Build
               .Context(StaticContext.Configure
                  .DataDirectory(@"C:\Users\Moi\source\repos\core\src\SampleData")
                  .Identity(() => new AuthIdentity(new Guid("c52a2874-bf95-4b50-9d45-a85a84309e75"), "Mike"))
               )
               .Create();
            KPCContext.Initialize(staticConfig);
            var context = KPCContext.Current;
            hello_world.ParseClass classer = new ParseClass(context);
            miracle(context);
        }
        public static void traitement(KitchenPC.Context.IKPCContext context)
        {
            hello_world.ParseClass classer = new ParseClass(context);
            String path = "C:/Users/Moi/Downloads/";
            String fichier = "rec_inglike";
            char numero = '1';
            var filename = path + fichier + numero + ".csv";
            classer.ParseUsageDoc(path + fichier + numero + ".csv", path + "POUBELLE_FICHIER" + numero + ".csv", path + "REC_FICHIER" + numero + ".csv");
            numero = '2';
            classer.ParseUsageDoc(path + fichier + numero + ".csv", path + "POUBELLE_FICHIER" + numero + ".csv", path + "REC_FICHIER" + numero + ".csv");
            numero = '3';
            classer.ParseUsageDoc(path + fichier + numero + ".csv", path + "POUBELLE_FICHIER" + numero + ".csv", path + "REC_FICHIER" + numero + ".csv");

        }
        public static void recyclage(KitchenPC.Context.IKPCContext context)
        {
            hello_world.ParseClass classer = new ParseClass(context);
            String path = "C:/Users/Moi/Downloads/";
            char numero = '1';
            classer.ParseUsageDoc(path + "Poubelle_" + numero + ".csv", path + "POUBELLE_FINALE" + numero + ".csv", path + "RECYCLAGE" + numero + ".csv");
            numero = '2';
            classer.ParseUsageDoc(path + "Poubelle_" + numero + ".csv", path + "POUBELLE_FINALE" + numero + ".csv", path + "RECYCLAGE" + numero + ".csv");
            numero = '3';
            classer.ParseUsageDoc(path + "Poubelle_" + numero + ".csv", path + "POUBELLE_FINALE" + numero + ".csv", path + "RECYCLAGE" + numero + ".csv");
            numero = '4';
            classer.ParseUsageDoc(path + "Poubelle_" + numero + ".csv", path + "POUBELLE_FINALE" + numero + ".csv", path + "RECYCLAGE" + numero + ".csv");

        }
        public static void trifinal(KitchenPC.Context.IKPCContext context, char numero)
        {
            String path = "C:/Users/Moi/Downloads/";
            String fichier = "POUBELLE_FINALE";
            var filename = path + fichier + numero + ".csv";
            Console.WriteLine("On commence " + filename);
            var poubellestring = new StringBuilder();
            var recettestring = new StringBuilder();
            var cpt_match = 0;
            var cpt_nomatch = 0;
            var i = 0;
            using (StreamReader sr = new StreamReader(filename))
            {
                String line;

                while ((line = sr.ReadLine()) != null)
                {
                    string[] parts = line.Split(',');
                    if (i != 0) //Ne pas lire le Header
                    {
                        try
                        {
                            var result = context.ParseIngredient(parts[1]);                      
                            var newLine = string.Format("{0};{1};{2}", parts[0], result.Name, result.Id);
                            recettestring.AppendLine(newLine);
                            cpt_match++;
                        }
                        catch
                        {
                            cpt_nomatch++;
                            var newLine = string.Format("{0},{1}", parts[0], parts[1]);
                            poubellestring.AppendLine(newLine);
                        }

                    }
                    i = i + 1;
                }
                Console.WriteLine("Match :" + cpt_match);
                Console.WriteLine("NoMatch :" + cpt_nomatch);
                File.WriteAllText(path+"elixir"+numero+".csv", recettestring.ToString());
                File.WriteAllText(path+"toxic"+numero+".csv", poubellestring.ToString());
            }
        }

        public static void miracle(KitchenPC.Context.IKPCContext context)
        {
            trifinal(context,'1');
            trifinal(context,'2');
            trifinal(context,'3');
            trifinal(context, '4');
        }
    }
}
