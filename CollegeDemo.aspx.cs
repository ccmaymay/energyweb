using System;
using System.ComponentModel;
using System.Drawing;
using ZedGraph;
using System.Data;
using System.Data.SqlClient;
using System.Configuration;
using System.Web;
using System.Web.Security;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Web.UI.WebControls.WebParts;
using System.Web.UI.HtmlControls;

namespace ZG1
{
    /// <summary>
    /// Summary description for graph.
    /// </summary>
    public partial class graph : System.Web.UI.Page
    {

        #region Web Form Designer generated code
        override protected void OnInit(EventArgs e)
        {
            //
            // CODEGEN: This call is required by the ASP.NET Web Form Designer.
            //
            InitializeComponent();
            base.OnInit(e);
        }

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
              this.ZedGraphWeb1.RenderGraph += new ZedGraph.Web.ZedGraphWebControlEventHandler(this.OnRenderGraph3);
        }
        #endregion

        /// <summary>
        /// This method is where you generate your graph.
        /// </summary>
        /// <param name="masterPane">You are provided with a MasterPane instance that
        /// contains one GraphPane by default (accessible via masterPane[0]).</param>
        /// <param name="g">A graphics instance so you can easily make the call to AxisChange()</param>
        /// <param name="z">And a ZedGraphWeb instance because the event handler requires it</param>
        /// 
//
//current rate graph:
//
        private void OnRenderGraph2(ZedGraph.Web.ZedGraphWeb z, System.Drawing.Graphics g, ZedGraph.MasterPane masterPane)
        {
            // Get the GraphPane so we can work with it
            GraphPane myPane = masterPane[0];

            // Set the title and axis labels
            myPane.Title.Text = "RATE MONITOR";
            myPane.YAxis.Title.Text = "DORM";
            myPane.XAxis.Title.Text = "AVERAGE WATTS LAST 10 SECONDS";

            // Create a TableAdapter instance to access the database
            SontagDbDataSetTableAdapters.MainTableTableAdapter sontagadapter =
                     new SontagDbDataSetTableAdapters.MainTableTableAdapter();
 
            // Create a TableAdapter instance to access the Case database
            CaseDbDataSetTableAdapters.MainTableTableAdapter caseadapter =
                    new CaseDbDataSetTableAdapters.MainTableTableAdapter();

            // Create a TableAdapter instance to access the Linde database
            LindeDbDataSetTableAdapters.MainTableTableAdapter lindeadapter =
                    new LindeDbDataSetTableAdapters.MainTableTableAdapter();

            // Create a TableAdapter instance to access the Atwood database
            AtwoodDbDataSetTableAdapters.MainTableTableAdapter atwoodadapter =
                     new AtwoodDbDataSetTableAdapters.MainTableTableAdapter();

 
            double sontagawatthr = Convert.ToDouble(sontagadapter.SontagAwatthr());
            double sontagbwatthr = Convert.ToDouble(sontagadapter.SontagBwatthr());
            double sontagcwatthr = Convert.ToDouble(sontagadapter.SontagCwatthr());
            double caseawatthr = Convert.ToDouble(caseadapter.CaseAwatthr());
            double casebwatthr = Convert.ToDouble(caseadapter.CaseBwatthr());
            double casecwatthr = Convert.ToDouble(caseadapter.CaseCwatthr());
            double lindeawatthr = Convert.ToDouble(lindeadapter.LindeAwatthr());
            double lindebwatthr = Convert.ToDouble(lindeadapter.LindeBwatthr());
            double lindecwatthr = Convert.ToDouble(lindeadapter.LindeCwatthr());
            double atwoodawatthr = Convert.ToDouble(atwoodadapter.AtwoodAwatthr());
            double atwoodbwatthr = Convert.ToDouble(atwoodadapter.AtwoodBwatthr());
            double atwoodcwatthr = Convert.ToDouble(atwoodadapter.AtwoodCwatthr());

            string[] labels = { "SONTAG", "CASE", "LINDE", "ATWOOD" };
            double[] x = { sontagawatthr, caseawatthr, lindeawatthr, atwoodawatthr};
            double[] x2 = { sontagbwatthr, casebwatthr, lindebwatthr, atwoodbwatthr };
            double[] x3 = { sontagcwatthr, casecwatthr, lindecwatthr, atwoodcwatthr };

            // Generate a red bar with "Curve 1" in the legend
            BarItem myCurve = myPane.AddBar("PHASE A", x, null, Color.Red);
            // Fill the bar with a red-white-red color gradient for a 3d look
            myCurve.Bar.Fill = new Fill(Color.Red, Color.White, Color.Red, 90f);

            // Generate a blue bar with "Curve 2" in the legend
            myCurve = myPane.AddBar("PHASE B", x2, null, Color.Blue);
            // Fill the bar with a Blue-white-Blue color gradient for a 3d look
            myCurve.Bar.Fill = new Fill(Color.Blue, Color.White, Color.Blue, 90f);

            // Generate a green bar with "Curve 3" in the legend
            myCurve = myPane.AddBar("PHASE C", x3, null, Color.Green);
            // Fill the bar with a Green-white-Green color gradient for a 3d look
            myCurve.Bar.Fill = new Fill(Color.Green, Color.White, Color.Green, 90f);

            // Draw the Y tics between the labels instead of at the labels
            myPane.YAxis.MajorTic.IsBetweenLabels = true;

            // Set the YAxis labels
            myPane.YAxis.Scale.TextLabels = labels;
            // Set the YAxis to Text type
            myPane.YAxis.Type = AxisType.Text;

            // Set the bar type to stack, which stacks the bars by automatically accumulating the values
            myPane.BarSettings.Type = BarType.Stack;

            // Make the bars horizontal by setting the BarBase to "Y"
            myPane.BarSettings.Base = BarBase.Y;

            // Fill the axis background with a color gradient
             myPane.Chart.Fill = new Fill(Color.White,
                 Color.FromArgb(255, 255, 166), 45.0F);

            masterPane.AxisChange(g);
        }
        /// <summary>
        /// Here is a completely independent second graph.  In InitializeComponent() above,
        /// ZedGraphWeb1 calls OnRenderGraph1, and ZedGraphWeb2 calls OnRenderGraph2.
        /// </summary>
        ///      
        private void OnRenderGraph3(ZedGraph.Web.ZedGraphWeb z, System.Drawing.Graphics g, ZedGraph.MasterPane masterPane)
        {
            // Get the GraphPane so we can work with it
            GraphPane myPane = masterPane[0];

            // Set the titles
            myPane.Title.Text = "WATTS LAST 4 HOURS";
            myPane.XAxis.Title.Text = "TIME";
            myPane.YAxis.Title.Text = "POWER(kW)";
///////////
/////////////////////////////////////////////Step1
///////////
            // Create a new DataSourcePointList to handle the database connection
            DataSourcePointList dsplsontag = new DataSourcePointList();

            DataSourcePointList dsplcase = new DataSourcePointList();

            DataSourcePointList dspllinde = new DataSourcePointList();

            DataSourcePointList dsplatwood = new DataSourcePointList();

            DataSourcePointList dsplsouth = new DataSourcePointList();

            DataSourcePointList dsplnorth1 = new DataSourcePointList();
            DataSourcePointList dsplnorth2 = new DataSourcePointList();
            DataSourcePointList dsplnorth3 = new DataSourcePointList();

            DataSourcePointList dsplwest1 = new DataSourcePointList();
            DataSourcePointList dsplwest2 = new DataSourcePointList();

            DataSourcePointList dspleast1 = new DataSourcePointList();
            DataSourcePointList dspleast2 = new DataSourcePointList();
            DataSourcePointList dspleast3 = new DataSourcePointList();

//////////////////////////////////////////Step2****must also do this from App_Code folder
////////////the name syntax is critical

            // Create a TableAdapter instance to access the database
            SontagDbDataSetTableAdapters.MainTableTableAdapter sontagadapter =
                     new SontagDbDataSetTableAdapters.MainTableTableAdapter();

            CaseDbDataSetTableAdapters.MainTableTableAdapter caseadapter =
                    new CaseDbDataSetTableAdapters.MainTableTableAdapter();

            LindeDbDataSetTableAdapters.MainTableTableAdapter lindeadapter =
                    new LindeDbDataSetTableAdapters.MainTableTableAdapter();

            AtwoodDbDataSetTableAdapters.MainTableTableAdapter atwoodadapter =
                     new AtwoodDbDataSetTableAdapters.MainTableTableAdapter();

            SouthDbDataSetTableAdapters.MainTableTableAdapter southadapter =
                     new SouthDbDataSetTableAdapters.MainTableTableAdapter();

            North1DbDataSetTableAdapters.MainTableTableAdapter north1adapter =
                     new North1DbDataSetTableAdapters.MainTableTableAdapter();
            North2DbDataSetTableAdapters.MainTableTableAdapter north2adapter =
                     new North2DbDataSetTableAdapters.MainTableTableAdapter();
            North3DbDataSetTableAdapters.MainTableTableAdapter north3adapter =
                     new North3DbDataSetTableAdapters.MainTableTableAdapter();

            West1DbDataSetTableAdapters.MainTableTableAdapter west1adapter =
                     new West1DbDataSetTableAdapters.MainTableTableAdapter();
            West2DbDataSetTableAdapters.MainTableTableAdapter west2adapter =
                     new West2DbDataSetTableAdapters.MainTableTableAdapter();

            East1DbDataSetTableAdapters.MainTableTableAdapter east1adapter =
                     new East1DbDataSetTableAdapters.MainTableTableAdapter();
            East2DbDataSetTableAdapters.MainTableTableAdapter east2adapter =
                     new East2DbDataSetTableAdapters.MainTableTableAdapter();
            East3DbDataSetTableAdapters.MainTableTableAdapter east3adapter =
                     new East3DbDataSetTableAdapters.MainTableTableAdapter();


//////////////////////////////////Step3

            // Create a DataTable and fill it with data from the database
            SontagDbDataSet.MainTableDataTable sontagtable = sontagadapter.GetData();

            CaseDbDataSet.MainTableDataTable casetable = caseadapter.GetData();

            LindeDbDataSet.MainTableDataTable lindetable = lindeadapter.GetData();

            AtwoodDbDataSet.MainTableDataTable atwoodtable = atwoodadapter.GetData();

            SouthDbDataSet.MainTableDataTable southtable = southadapter.GetData();

            North1DbDataSet.MainTableDataTable north1table = north1adapter.GetData();
            North2DbDataSet.MainTableDataTable north2table = north2adapter.GetData();
            North3DbDataSet.MainTableDataTable north3table = north3adapter.GetData();

            East1DbDataSet.MainTableDataTable east1table = east1adapter.GetData();
            East2DbDataSet.MainTableDataTable east2table = east2adapter.GetData();
            East3DbDataSet.MainTableDataTable east3table = east3adapter.GetData();
      
            West1DbDataSet.MainTableDataTable west1table = west1adapter.GetData();
            West2DbDataSet.MainTableDataTable west2table = west2adapter.GetData();


//////////////////////////////////////Initialize graph display variables


            dsplsontag.DataSource = sontagtable;
            dsplsontag.XDataMember = "COL1";
            dsplsontag.YDataMember = "Expr1";
            dsplsontag.ZDataMember = null;

            dsplcase.DataSource = casetable;
            dsplcase.XDataMember = "COL1";
            dsplcase.YDataMember = "Expr1";
            dsplcase.ZDataMember = null;

            dspllinde.DataSource = lindetable;
            dspllinde.XDataMember = "COL1";
            dspllinde.YDataMember = "Expr1";
            dspllinde.ZDataMember = null;

            dsplatwood.DataSource = atwoodtable;
            dsplatwood.XDataMember = "COL1";
            dsplatwood.YDataMember = "Expr1";
            dsplatwood.ZDataMember = null;

            dsplsouth.DataSource = southtable;
            dsplsouth.XDataMember = "COL1";
            dsplsouth.YDataMember = "Expr1";
            dsplsouth.ZDataMember = null;

            dsplnorth1.DataSource = north1table;
            dsplnorth1.XDataMember = "COL1";
            dsplnorth1.YDataMember = "Expr1";
            dsplnorth1.ZDataMember = null;
            dsplnorth2.DataSource = north2table;
            dsplnorth2.XDataMember = "COL1";
            dsplnorth2.YDataMember = "Expr1";
            dsplnorth2.ZDataMember = null;
            dsplnorth3.DataSource = north3table;
            dsplnorth3.XDataMember = "COL1";
            dsplnorth3.YDataMember = "Expr1";
            dsplnorth3.ZDataMember = null;


            dspleast1.DataSource = east1table;
            dspleast1.XDataMember = "COL1";
            dspleast1.YDataMember = "Expr1";
            dspleast1.ZDataMember = null;
            dspleast2.DataSource = east2table;
            dspleast2.XDataMember = "COL1";
            dspleast2.YDataMember = "Expr1";
            dspleast2.ZDataMember = null;

            dspleast3.DataSource = east3table;
            dspleast3.XDataMember = "COL1";
            dspleast3.YDataMember = "Expr1";
            dspleast3.ZDataMember = null;

            dsplwest1.DataSource = west1table;
            dsplwest1.XDataMember = "COL1";
            dsplwest1.YDataMember = "Expr1";
            dsplwest1.ZDataMember = null;
            dsplwest2.DataSource = west2table;
            dsplwest2.XDataMember = "COL1";
            dsplwest2.YDataMember = "Expr1";
            dsplwest2.ZDataMember = null;

            // X axis will be dates
            myPane.XAxis.Type = AxisType.Date;

            // Make a curve
            LineItem myCurve = myPane.AddCurve("SONTAG", dsplsontag, Color.Blue, SymbolType.Circle);
            // Turn off the line so it's a scatter plot
            myCurve.Line.IsVisible = true;
            // Set symbol size
            myCurve.Symbol.Size = 1.0F;

            LineItem myCurve2 = myPane.AddCurve("CASE", dsplcase, Color.Red);
            myCurve2.Line.IsVisible = true;
            myCurve2.Symbol.Size = 1.0F;

            LineItem myCurve3 = myPane.AddCurve("LINDE", dspllinde, Color.Green);
            myCurve3.Line.IsVisible = true;
            myCurve3.Symbol.Size = 1.0F;

            LineItem myCurve4 = myPane.AddCurve("ATWOOD", dsplatwood, Color.Yellow);
            myCurve4.Line.IsVisible = true;
            myCurve4.Symbol.Size = 1.0F;

            LineItem myCurve5 = myPane.AddCurve("SOUTH", dsplsouth, Color.Black);
            myCurve5.Line.IsVisible = true;
            myCurve5.Symbol.Size = 1.0F;

            LineItem myCurve6 = myPane.AddCurve("NORTH1", dsplnorth1, Color.Purple);
            myCurve6.Line.IsVisible = true;
            myCurve6.Symbol.Size = 1.0F;
            LineItem myCurve7 = myPane.AddCurve("NORTH2", dsplnorth2, Color.Pink);
            myCurve7.Line.IsVisible = true;
            myCurve7.Symbol.Size = 1.0F;
            LineItem myCurve8 = myPane.AddCurve("NORTH HVAC", dsplnorth3, Color.Silver);
            myCurve8.Line.IsVisible = true;
            myCurve8.Symbol.Size = 1.0F;

            LineItem myCurve9 = myPane.AddCurve("EAST1", dspleast1, Color.Olive);
            myCurve9.Line.IsVisible = true;
            myCurve9.Symbol.Size = 1.0F;
            LineItem myCurve10 = myPane.AddCurve("EAST2", dspleast2, Color.Turquoise);
            myCurve10.Line.IsVisible = true;
            myCurve10.Symbol.Size = 1.0F;

            LineItem myCurve11 = myPane.AddCurve("WEST1", dsplwest1, Color.Teal);
            myCurve11.Line.IsVisible = true;
            myCurve11.Symbol.Size = 1.0F;
            LineItem myCurve12 = myPane.AddCurve("WEST2", dsplwest2, Color.Lime);
            myCurve12.Line.IsVisible = true;
            myCurve12.Symbol.Size = 1.0F;
            LineItem myCurve13 = myPane.AddCurve("WEST HVAC", dspleast3, Color.Fuchsia);
            myCurve13.Line.IsVisible = true;
            myCurve13.Symbol.Size = 1.0F;

            // Auto set the scale ranges
            myPane.AxisChange();
            // Fill the axis background with a gradient
            //myPane.Chart.Fill = new Fill(Color.White, Color.LightGoldenrodYellow, 45.0f);

        }


}
}