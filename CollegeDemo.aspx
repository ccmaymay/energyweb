<%@ Page Language="c#" Inherits="ZG1.graph" CodeFile="CollegeDemo.aspx.cs" %>
<%@ Register TagPrefix="zgw" Namespace="ZedGraph.Web" Assembly="ZedGraph.Web" %>

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" >
<html>

<head id="Head1" runat="server">
    <title>WEB Distributed Wireless Electric Utility Monitoring</title>
    <meta http-equiv="refresh" content="100" >
<script language="javascript" type="text/javascript">

</script>
</head>
   <body>
    <form id="form1" runat="server">
    <div>
                   <!-- #include file="header.aspx" --> 
<table style="width: 676px; height: 117px">
            <tr>
                <td colspan="3" rowspan="3">

       <ZGW:ZEDGRAPHWEB id="ZedGraphWeb1" runat="server" RenderMode="ImageTag"
            Width="1840" Height="650">
           <XAxis AxisColor="Black" Cross="0" CrossAuto="True" IsOmitMag="False" IsPreventLabelOverlap="True"
               IsShowTitle="True" IsTicsBetweenLabels="True" IsUseTenPower="False" IsVisible="True"
               IsZeroLine="False" MinSpace="0" Title="" Type="Linear">
               <FontSpec Angle="0" Family="Arial" FontColor="Black" IsBold="True" IsItalic="False"
                   IsUnderline="False" Size="14" StringAlignment="Center">
                   <Border Color="Black" InflateFactor="0" IsVisible="False" Width="1" />
                   <Fill AlignH="Center" AlignV="Center" Color="White" ColorOpacity="100" IsScaled="True"
                       IsVisible="True" RangeMax="0" RangeMin="0" Type="None" />
               </FontSpec>
               <MinorGrid Color="Black" DashOff="5" DashOn="1" IsVisible="False" PenWidth="1" />
               <MajorGrid Color="Black" DashOff="5" DashOn="1" IsVisible="False" PenWidth="1" />
               <MinorTic Color="Black" IsInside="True" IsOpposite="True" IsOutside="True" PenWidth="1"
                   Size="5" />
               <MajorTic Color="Black" IsInside="True" IsOpposite="True" IsOutside="True" PenWidth="1"
                   Size="5" />
               <Scale Align="Center" Format="g" FormatAuto="True" IsReverse="False" Mag="0" MagAuto="True"
                   MajorStep="1" MajorStepAuto="True" MajorUnit="Day" Max="0" MaxAuto="True" MaxGrace="0.1"
                   Min="0" MinAuto="True" MinGrace="0.1" MinorStep="1" MinorStepAuto="True" MinorUnit="Day">
                   <FontSpec Angle="0" Family="Arial" FontColor="Black" IsBold="False" IsItalic="False"
                       IsUnderline="False" Size="14" StringAlignment="Center">
                       <Border Color="Black" InflateFactor="0" IsVisible="False" Width="1" />
                       <Fill AlignH="Center" AlignV="Center" Color="White" ColorOpacity="100" IsScaled="True"
                           IsVisible="True" RangeMax="0" RangeMin="0" Type="None" />
                   </FontSpec>
               </Scale>
           </XAxis>
           <Y2Axis AxisColor="Black" Cross="0" CrossAuto="True" IsOmitMag="False" IsPreventLabelOverlap="True"
               IsShowTitle="True" IsTicsBetweenLabels="True" IsUseTenPower="False" IsVisible="False"
               IsZeroLine="True" MinSpace="0" Title="" Type="Linear">
               <FontSpec Angle="0" Family="Arial" FontColor="Black" IsBold="True" IsItalic="False"
                   IsUnderline="False" Size="14" StringAlignment="Center">
                   <Border Color="Black" InflateFactor="0" IsVisible="False" Width="1" />
                   <Fill AlignH="Center" AlignV="Center" Color="White" ColorOpacity="100" IsScaled="True"
                       IsVisible="True" RangeMax="0" RangeMin="0" Type="None" />
               </FontSpec>
               <MinorGrid Color="Black" DashOff="5" DashOn="1" IsVisible="False" PenWidth="1" />
               <MajorGrid Color="Black" DashOff="5" DashOn="1" IsVisible="False" PenWidth="1" />
               <MinorTic Color="Black" IsInside="True" IsOpposite="True" IsOutside="True" PenWidth="1"
                   Size="5" />
               <MajorTic Color="Black" IsInside="True" IsOpposite="True" IsOutside="True" PenWidth="1"
                   Size="5" />
               <Scale Align="Center" Format="g" FormatAuto="True" IsReverse="False" Mag="0" MagAuto="True"
                   MajorStep="1" MajorStepAuto="True" MajorUnit="Day" Max="0" MaxAuto="True" MaxGrace="0.1"
                   Min="0" MinAuto="True" MinGrace="0.1" MinorStep="1" MinorStepAuto="True" MinorUnit="Day">
                   <FontSpec Angle="-90" Family="Arial" FontColor="Black" IsBold="False" IsItalic="False"
                       IsUnderline="False" Size="14" StringAlignment="Center">
                       <Border Color="Black" InflateFactor="0" IsVisible="False" Width="1" />
                       <Fill AlignH="Center" AlignV="Center" Color="White" ColorOpacity="100" IsScaled="True"
                           IsVisible="True" RangeMax="0" RangeMin="0" Type="None" />
                   </FontSpec>
               </Scale>
           </Y2Axis>
           <FontSpec Angle="0" Family="Arial" FontColor="Black" IsBold="True" IsItalic="False"
               IsUnderline="False" Size="16" StringAlignment="Center">
               <Border Color="Black" InflateFactor="0" IsVisible="False" Width="1" />
               <Fill AlignH="Center" AlignV="Center" Color="White" ColorOpacity="100" IsScaled="True"
                   IsVisible="True" RangeMax="0" RangeMin="0" Type="None" />
           </FontSpec>
           <MasterPaneFill AlignH="Center" AlignV="Center" Color="White" ColorOpacity="100"
               IsScaled="True" IsVisible="True" RangeMax="0" RangeMin="0" Type="Solid" />
           <YAxis AxisColor="Black" Cross="0" CrossAuto="True" IsOmitMag="False" IsPreventLabelOverlap="True"
               IsShowTitle="True" IsTicsBetweenLabels="True" IsUseTenPower="False" IsVisible="True"
               IsZeroLine="True" MinSpace="0" Title="" Type="Linear">
               <FontSpec Angle="-180" Family="Arial" FontColor="Black" IsBold="True" IsItalic="False"
                   IsUnderline="False" Size="14" StringAlignment="Center">
                   <Border Color="Black" InflateFactor="0" IsVisible="False" Width="1" />
                   <Fill AlignH="Center" AlignV="Center" Color="White" ColorOpacity="100" IsScaled="True"
                       IsVisible="True" RangeMax="0" RangeMin="0" Type="None" />
               </FontSpec>
               <MinorGrid Color="Black" DashOff="5" DashOn="1" IsVisible="False" PenWidth="1" />
               <MajorGrid Color="Black" DashOff="5" DashOn="1" IsVisible="False" PenWidth="1" />
               <MinorTic Color="Black" IsInside="True" IsOpposite="True" IsOutside="True" PenWidth="1"
                   Size="5" />
               <MajorTic Color="Black" IsInside="True" IsOpposite="True" IsOutside="True" PenWidth="1"
                   Size="5" />
               <Scale Align="Center" Format="g" FormatAuto="True" IsReverse="False" Mag="0" MagAuto="True"
                   MajorStep="1" MajorStepAuto="True" MajorUnit="Day" Max="0" MaxAuto="True" MaxGrace="0.1"
                   Min="0" MinAuto="True" MinGrace="0.1" MinorStep="1" MinorStepAuto="True" MinorUnit="Day">
                   <FontSpec Angle="90" Family="Arial" FontColor="Black" IsBold="False" IsItalic="False"
                       IsUnderline="False" Size="14" StringAlignment="Center">
                       <Border Color="Black" InflateFactor="0" IsVisible="False" Width="1" />
                       <Fill AlignH="Center" AlignV="Center" Color="White" ColorOpacity="100" IsScaled="True"
                           IsVisible="True" RangeMax="0" RangeMin="0" Type="None" />
                   </FontSpec>
               </Scale>
           </YAxis>
           <Legend IsHStack="True" IsReverse="False" IsVisible="True" Position="Top">
               <Location AlignH="Left" AlignV="Center" CoordinateFrame="ChartFraction" Height="0"
                   Width="0" X="0" Y="0">
                   <TopLeft X="0" Y="0" />
                   <BottomRight X="0" Y="0" />
               </Location>
               <FontSpec Angle="0" Family="Arial" FontColor="Black" IsBold="False" IsItalic="False"
                   IsUnderline="False" Size="12" StringAlignment="Center">
                   <Border Color="Black" InflateFactor="0" IsVisible="False" Width="1" />
                   <Fill AlignH="Center" AlignV="Center" Color="White" ColorOpacity="100" IsScaled="True"
                       IsVisible="True" RangeMax="0" RangeMin="0" Type="Solid" />
               </FontSpec>
               <Fill AlignH="Center" AlignV="Center" Color="White" ColorOpacity="100" IsScaled="True"
                   IsVisible="True" RangeMax="0" RangeMin="0" Type="Brush" />
               <Border Color="Black" InflateFactor="0" IsVisible="True" Width="1" />
           </Legend>
           <PaneFill AlignH="Center" AlignV="Center" Color="White" ColorOpacity="100" IsScaled="True"
               IsVisible="True" RangeMax="0" RangeMin="0" Type="Solid" />
           <ChartFill AlignH="Center" AlignV="Center" Color="White" ColorOpacity="100" IsScaled="True"
               IsVisible="True" RangeMax="0" RangeMin="0" Type="Brush" />
           <ChartBorder Color="Black" InflateFactor="0" IsVisible="True" Width="1" />
           <MasterPaneBorder Color="Black" InflateFactor="0" IsVisible="True" Width="1" />
           <Margins Bottom="10" Left="10" Right="10" Top="10" />
           <PaneBorder Color="Black" InflateFactor="0" IsVisible="True" Width="1" />
       </ZGW:ZEDGRAPHWEB> 
                </td>
            </tr>
            <tr>
            </tr>
            <tr>
            </tr>
        </table>
        <br />
        <table border="2" bordercolor="navy" style="width: 1px; height: 92px">
            <tr>
                <td style="width: 246px; height: 10px">
                    <span style="font-size: 9pt">DORM</span></td>
                <td style="width: 16px; height: 10px">
                    <span style="color: windowtext">
                    ATWOOD</span></td>
                <td style="width: 16px; height: 10px">
                    <span style="color: windowtext">
                    CASE</span></td>
                <td style="width: 16px; height: 10px">
                    <span style="color: menutext">
                    LINDE</span></td>
                <td style="width: 16px; height: 10px">
                    <span style="color: menutext">
                    SONTAG</span></td>
                <td style="width: 16px; height: 10px">
                    NORTH</td>
                <td style="width: 16px; height: 10px">
                    SOUTH</td>
                <td style="width: 16px; height: 10px">
                    EAST</td>
                <td style="width: 16px; height: 10px">
                    WEST</td>
            </tr>
            <tr>
                <td style="width: 246px; height: 10px">
                    LAST 24 HOURS</td>
                <td style="width: 16px; height: 10px">
                    <asp:TextBox ID="TextBox1" runat="server">0</asp:TextBox></td>
                <td style="width: 16px; height: 10px">
                    <asp:TextBox ID="TextBox2" runat="server">0</asp:TextBox></td>
                <td style="width: 16px; height: 10px">
                    <asp:TextBox ID="TextBox3" runat="server">0</asp:TextBox></td>
                <td style="width: 16px; height: 10px">
                    <asp:TextBox ID="TextBox4" runat="server">0</asp:TextBox></td>
                <td style="width: 16px; height: 10px">
                    <asp:TextBox ID="TextBox5" runat="server">0</asp:TextBox></td>
                <td style="width: 16px; height: 10px">
                    <asp:TextBox ID="TextBox6" runat="server">0</asp:TextBox></td>
                <td style="width: 16px; height: 10px">
                    <asp:TextBox ID="TextBox7" runat="server">0</asp:TextBox></td>
                <td style="width: 16px; height: 10px">
                    <asp:TextBox ID="TextBox8" runat="server">0</asp:TextBox></td>
            </tr>
            <tr>
                <td style="width: 16px; height: 12px">
                    <span style="font-size: 9pt">
                    AVE KWATTS
                        SINCE</span>
                                               
                        <asp:DetailsView ID="DetailsView1" runat="server" AutoGenerateRows="False" 
                        DataSourceID="SqlDataSource1" Height="20px" Width="40px" BackColor="White" BorderColor="White" BorderStyle="Ridge" BorderWidth="2px" CellPadding="3" CellSpacing="1" GridLines="None" >
                            <Fields>
                                <asp:BoundField DataField="col1" SortExpression="col1" />
                            </Fields>
                            <FooterStyle BackColor="#C6C3C6" ForeColor="Black" />
                            <RowStyle BackColor="#DEDFDE" ForeColor="Black" />
                            <PagerStyle BackColor="#C6C3C6" ForeColor="Black" HorizontalAlign="Right" />
                            <HeaderStyle BackColor="#4A3C8C" Font-Bold="True" ForeColor="#E7E7FF" />
                            <EditRowStyle BackColor="#9471DE" Font-Bold="True" ForeColor="White" />
                        </asp:DetailsView>
                    &nbsp;
                    
                        <asp:SqlDataSource ID="SqlDataSource1" runat="server" ConnectionString="<%$ ConnectionStrings:SontagDbConnectionString %>"
                            SelectCommand="select top 1 col1&#13;&#10;from maintable"></asp:SqlDataSource> 
                </td>
                <td style="width: 16px; height: 12px">
                        <asp:DetailsView ID="DetailsView2" runat="server" AutoGenerateRows="False" DataSourceID="SqlDataSource2"
                            Height="20px" Width="40px"  BackColor="White" BorderColor="White" BorderStyle="Ridge" BorderWidth="2px" CellPadding="3" CellSpacing="1" GridLines="None">
                            <Fields>
                                <asp:BoundField DataField="Column1" DataFormatString="{0:F3}"
                                    ReadOnly="True" SortExpression="Column1" />
                            </Fields>
                            <FooterStyle BackColor="#C6C3C6" ForeColor="Black" />
                            <RowStyle BackColor="#DEDFDE" ForeColor="Black" />
                            <PagerStyle BackColor="#C6C3C6" ForeColor="Black" HorizontalAlign="Right" />
                            <HeaderStyle BackColor="#4A3C8C" Font-Bold="True" ForeColor="#E7E7FF" />
                            <EditRowStyle BackColor="#9471DE" Font-Bold="True" ForeColor="White" />
                        </asp:DetailsView>
                    &nbsp;
                <asp:SqlDataSource ID="SqlDataSource2" runat="server" ConnectionString="<%$ ConnectionStrings:AtwoodDbConnectionString %>"
                            SelectCommand="SELECT  .01*( Sum(Col3)+Sum(col4)+Sum(col5) )/(datediff(second, MIN(COL1), MAX(Col1)) )&#13;&#10;FROM MAINTABLE"  >
                        </asp:SqlDataSource>                       
                </td>
                <td style="width: 146px; height: 12px">
                    <asp:DetailsView ID="DetailsView3" runat="server" AutoGenerateRows="False"
                            DataSourceID="SqlDataSource3" Height="20px" Width="40px"  BackColor="White" BorderColor="White" BorderStyle="Ridge" BorderWidth="2px" CellPadding="3" CellSpacing="1" GridLines="None"  >
                            <Fields>
                                <asp:BoundField DataField="Column1" DataFormatString="{0:F3}"
                                    ReadOnly="True" SortExpression="Column1" />
                            </Fields>
                        <FooterStyle BackColor="#C6C3C6" ForeColor="Black" />
                        <RowStyle BackColor="#DEDFDE" ForeColor="Black" />
                        <PagerStyle BackColor="#C6C3C6" ForeColor="Black" HorizontalAlign="Right" />
                        <HeaderStyle BackColor="#4A3C8C" Font-Bold="True" ForeColor="#E7E7FF" />
                        <EditRowStyle BackColor="#9471DE" Font-Bold="True" ForeColor="White" />
                        </asp:DetailsView>
                        <asp:SqlDataSource ID="SqlDataSource3" runat="server" ConnectionString="<%$ ConnectionStrings:CaseDbConnectionString %>"
                            SelectCommand="SELECT  .01*( Sum(Col3)+Sum(col4)+Sum(col5) )/(datediff(second, MIN(COL1), MAX(Col1)) )&#13;&#10;FROM MAINTABLE">
                        </asp:SqlDataSource>
                </td>
                <td style="width: 16px; height: 12px">
                        <asp:DetailsView ID="DetailsView4" runat="server" AutoGenerateRows="False" DataSourceID="SqlDataSource4"
                            Height="20px" Width="40px" BackColor="White" BorderColor="White" BorderStyle="Ridge" BorderWidth="2px" CellPadding="3" CellSpacing="1" GridLines="None">
                            <Fields>
                                <asp:BoundField DataField="Column1" ReadOnly="True" SortExpression="Column1" DataFormatString="{0:F3} " />
                            </Fields>
                            <FooterStyle BackColor="#C6C3C6" ForeColor="Black" />
                            <RowStyle BackColor="#DEDFDE" ForeColor="Black" />
                            <PagerStyle BackColor="#C6C3C6" ForeColor="Black" HorizontalAlign="Right" />
                            <HeaderStyle BackColor="#4A3C8C" Font-Bold="True" ForeColor="#E7E7FF" />
                            <EditRowStyle BackColor="#9471DE" Font-Bold="True" ForeColor="White" />
                        </asp:DetailsView>
                        <asp:SqlDataSource ID="SqlDataSource4" runat="server" ConnectionString="<%$ ConnectionStrings:LindeDbConnectionString %>"
                            SelectCommand="SELECT  .01*( Sum(Col3)+Sum(col4)+Sum(col5) )/(datediff(second, MIN(COL1), MAX(Col1)) )&#13;&#10;FROM MAINTABLE">
                        </asp:SqlDataSource>
                </td>
                <td style="width: 16px; height: 12px">
                        <asp:DetailsView ID="DetailsView5" runat="server" AutoGenerateRows="False" DataSourceID="SqlDataSource5"
                            Height="20px" Width="40px" BackColor="White" BorderColor="White" BorderStyle="Ridge" BorderWidth="2px" CellPadding="3" CellSpacing="1" GridLines="None" >
                            <Fields>
                                <asp:BoundField DataField="Column1" ReadOnly="True" SortExpression="Column1" DataFormatString="{0:F3} " />
                            </Fields>
                            <FooterStyle BackColor="#C6C3C6" ForeColor="Black" />
                            <RowStyle BackColor="#DEDFDE" ForeColor="Black" />
                            <PagerStyle BackColor="#C6C3C6" ForeColor="Black" HorizontalAlign="Right" />
                            <HeaderStyle BackColor="#4A3C8C" Font-Bold="True" ForeColor="#E7E7FF" />
                            <EditRowStyle BackColor="#9471DE" Font-Bold="True" ForeColor="White" />
                        </asp:DetailsView>
                        <asp:SqlDataSource ID="SqlDataSource5" runat="server" ConnectionString="<%$ ConnectionStrings:SontagDbConnectionString %>"
                            SelectCommand="SELECT .01*( Sum(Col3)+Sum(col4)+Sum(col5) )/(datediff(second, MIN(COL1), MAX(Col1)) )&#13;&#10;FROM MAINTABLE">
                        </asp:SqlDataSource>
                </td>
                <td style="width: 16px; height: 12px">
                    <asp:DetailsView ID="DetailsView12" runat="server" AutoGenerateRows="False" BackColor="White"
                        BorderColor="White" BorderStyle="Ridge" BorderWidth="2px" CellPadding="3" CellSpacing="1"
                        DataSourceID="SqlDataSource12" GridLines="None" Height="20px" Width="40px" >
                        <FooterStyle BackColor="#C6C3C6" ForeColor="Black" />
                        <RowStyle BackColor="#DEDFDE" ForeColor="Black" />
                        <PagerStyle BackColor="#C6C3C6" ForeColor="Black" HorizontalAlign="Right" />
                        <Fields>
                            <asp:BoundField DataField="Column1" DataFormatString="{0:F3}" HeaderText="NORTH1"
                                ReadOnly="True" SortExpression="Column1" />
                        </Fields>
                        <HeaderStyle BackColor="#4A3C8C" Font-Bold="True" ForeColor="#E7E7FF" />
                        <EditRowStyle BackColor="#9471DE" Font-Bold="True" ForeColor="White" />
                    </asp:DetailsView>
                    <asp:SqlDataSource ID="SqlDataSource12" runat="server" ConnectionString="<%$ ConnectionStrings:North1DbConnectionString %>"
                        SelectCommand="SELECT  .01*( Sum(Col3)+Sum(col4)+Sum(col5) )/(datediff(second, MIN(COL1), MAX(Col1)) )&#13;&#10;FROM MAINTABLE">
                    </asp:SqlDataSource>
                    <asp:DetailsView ID="DetailsView13" runat="server" AutoGenerateRows="False" BackColor="White"
                        BorderColor="White" BorderStyle="Ridge" BorderWidth="2px" CellPadding="3" CellSpacing="1"
                        DataSourceID="SqlDataSource13" GridLines="None" Height="10px" Width="40px">
                        <FooterStyle BackColor="#C6C3C6" ForeColor="Black" />
                        <RowStyle BackColor="#DEDFDE" ForeColor="Black" />
                        <PagerStyle BackColor="#C6C3C6" ForeColor="Black" HorizontalAlign="Right" />
                        <Fields>
                            <asp:BoundField DataField="Column1" DataFormatString="{0:F3}" HeaderText="NORTH2"
                                SortExpression="Column1" />
                        </Fields>
                        <HeaderStyle BackColor="#4A3C8C" Font-Bold="True" ForeColor="#E7E7FF" />
                        <EditRowStyle BackColor="#9471DE" Font-Bold="True" ForeColor="White" />
                    </asp:DetailsView>
                    <asp:SqlDataSource ID="SqlDataSource13" runat="server" ConnectionString="<%$ ConnectionStrings:North2DbConnectionString %>"
                        SelectCommand="SELECT  .01*( Sum(Col3)+Sum(col4) )/(datediff(second, MIN(COL1), MAX(Col1)) )&#13;&#10;FROM MAINTABLE">
                    </asp:SqlDataSource>
                    <asp:DetailsView ID="DetailsView14" runat="server" AutoGenerateRows="False" BackColor="White"
                        BorderColor="White" BorderStyle="Ridge" BorderWidth="2px" CellPadding="3" CellSpacing="1"
                        DataSourceID="SqlDataSource14" GridLines="None" Height="10px" 
                        Width="40px">
                        <FooterStyle BackColor="#C6C3C6" ForeColor="Black" />
                        <RowStyle BackColor="#DEDFDE" ForeColor="Black" />
                        <PagerStyle BackColor="#C6C3C6" ForeColor="Black" HorizontalAlign="Right" />
                        <Fields>
                            <asp:BoundField DataField="Column1" DataFormatString="{0:F3}" HeaderText="HVAC    "
                                ReadOnly="True" SortExpression="Column1" />
                        </Fields>
                        <HeaderStyle BackColor="#4A3C8C" Font-Bold="True" ForeColor="#E7E7FF" />
                        <EditRowStyle BackColor="#9471DE" Font-Bold="True" ForeColor="White" />
                    </asp:DetailsView>
                    <asp:SqlDataSource ID="SqlDataSource14" runat="server" ConnectionString="<%$ ConnectionStrings:North3DbConnectionString %>"
                        SelectCommand="SELECT  .01*( Sum(Col3)+Sum(col4)+Sum(col5) )/(datediff(second, MIN(COL1), MAX(Col1)) )&#13;&#10;FROM MAINTABLE">
                    </asp:SqlDataSource>
                    <asp:DetailsView ID="DetailsView16" runat="server" AutoGenerateRows="False" DataSourceID="SqlDataSource16"
                        Height="26px" Width="125px">
                        <Fields>
                            <asp:BoundField DataField="Total" DataFormatString="{0:F3}" HeaderText="Total" ReadOnly="True"
                                SortExpression="Total" />
                        </Fields>
                    </asp:DetailsView>
                    <asp:SqlDataSource ID="SqlDataSource16" runat="server" ConnectionString="<%$ ConnectionStrings:North1DbConnectionString %>"
                        SelectCommand="select (Select   .01*( Sum(Col3)+Sum(col4)+Sum(col5) )/(datediff(second, MIN(COL1), MAX(Col1)) )&#13;&#10;FROM North1DB.dbo.MAINTABLE ) +&#13;&#10;&#13;&#10;(select .01*( Sum(Col3)+Sum(col4)+Sum(col5) )/(datediff(second, MIN(COL1), MAX(Col1)) )&#13;&#10;FROM North2DB.dbo.MAINTABLE ) +&#13;&#10;&#13;&#10;(select .01*( Sum(Col3)+Sum(col4)+Sum(col5) )/(datediff(second, MIN(COL1), MAX(Col1)) )&#13;&#10;FROM North3DB.dbo.MAINTABLE )&#13;&#10;&#13;&#10;as Total">
                    </asp:SqlDataSource>
                </td>
                <td style="width: 16px; height: 12px">
                        <asp:DetailsView ID="DetailsView6" runat="server" AutoGenerateRows="False" DataSourceID="SqlDataSource6"
                            Height="10px" Width="40px" BackColor="White" BorderColor="White" BorderStyle="Ridge" BorderWidth="2px" CellPadding="3" CellSpacing="1" GridLines="None">
                            <Fields>
                                <asp:BoundField DataField="Column1" DataFormatString="{0:F3} "
                                    ReadOnly="True" SortExpression="Column1" />
                            </Fields>
                            <FooterStyle BackColor="#C6C3C6" ForeColor="Black" />
                            <RowStyle BackColor="#DEDFDE" ForeColor="Black" />
                            <PagerStyle BackColor="#C6C3C6" ForeColor="Black" HorizontalAlign="Right" />
                            <HeaderStyle BackColor="#4A3C8C" Font-Bold="True" ForeColor="#E7E7FF" />
                            <EditRowStyle BackColor="#9471DE" Font-Bold="True" ForeColor="White" />
                        </asp:DetailsView>
                        <asp:SqlDataSource ID="SqlDataSource6" runat="server" ConnectionString="<%$ ConnectionStrings:SouthDbConnectionString %>"
                            SelectCommand="SELECT  .01*( Sum(Col3)+Sum(col4)+Sum(col5) )/(datediff(second, MIN(COL1), MAX(Col1)) )&#13;&#10;FROM MAINTABLE">
                        </asp:SqlDataSource>
                </td>
                <td style="width: 16px; height: 12px">
                    <asp:DetailsView ID="DetailsView10" runat="server" AutoGenerateRows="False" BackColor="White"
                        BorderColor="White" BorderStyle="Ridge" BorderWidth="2px" CellPadding="3" CellSpacing="1"
                        DataSourceID="SqlDataSource10" GridLines="None" Height="20px" Width="40px">
                        <FooterStyle BackColor="#C6C3C6" ForeColor="Black" />
                        <RowStyle BackColor="#DEDFDE" ForeColor="Black" />
                        <PagerStyle BackColor="#C6C3C6" ForeColor="Black" HorizontalAlign="Right" />
                        <Fields>
                            <asp:BoundField DataField="Column1" DataFormatString="{0:F3}" HeaderText="East1"
                                ReadOnly="True" SortExpression="Column1" />
                        </Fields>
                        <HeaderStyle BackColor="#4A3C8C" Font-Bold="True" ForeColor="#E7E7FF" />
                        <EditRowStyle BackColor="#9471DE" Font-Bold="True" ForeColor="White" />
                    </asp:DetailsView>
                    <asp:SqlDataSource ID="SqlDataSource10" runat="server" ConnectionString="<%$ ConnectionStrings:East1DbConnectionString %>"
                        SelectCommand="Select   .01*( Sum(Col3)+Sum(col4)+Sum(col5) )/(datediff(second, MIN(COL1), MAX(Col1)) )&#13;&#10;FROM East1DB.dbo.MAINTABLE&#13;&#10;&#13;&#10;">
                    </asp:SqlDataSource>
                    <asp:DetailsView ID="DetailsView11" runat="server" AutoGenerateRows="False" BackColor="White"
                        BorderColor="White" BorderStyle="Ridge" BorderWidth="2px" CellPadding="3" CellSpacing="1"
                        DataSourceID="SqlDataSource11" GridLines="None" Height="20px" Width="40px">
                        <FooterStyle BackColor="#C6C3C6" ForeColor="Black" />
                        <RowStyle BackColor="#DEDFDE" ForeColor="Black" />
                        <PagerStyle BackColor="#C6C3C6" ForeColor="Black" HorizontalAlign="Right" />
                        <Fields>
                            <asp:BoundField DataField="Column1" DataFormatString="{0:F3}" HeaderText="EAST2"
                                ReadOnly="True" SortExpression="Column1" />
                        </Fields>
                        <HeaderStyle BackColor="#4A3C8C" Font-Bold="True" ForeColor="#E7E7FF" />
                        <EditRowStyle BackColor="#9471DE" Font-Bold="True" ForeColor="White" />
                    </asp:DetailsView>
                    <asp:SqlDataSource ID="SqlDataSource11" runat="server" ConnectionString="<%$ ConnectionStrings:East2DbConnectionString %>"
                        SelectCommand="SELECT  .01*( Sum(Col3)+Sum(col4))/(datediff(second, MIN(COL1), MAX(Col1)) )&#13;&#10;FROM MAINTABLE">
                    </asp:SqlDataSource>
                    &nbsp;&nbsp;&nbsp;<asp:DetailsView ID="DetailsView15" runat="server" AutoGenerateRows="False"
                        DataSourceID="SqlDataSource15" Height="25px" Width="125px">
                        <Fields>
                            <asp:BoundField DataField="Total" DataFormatString="{0:F3}" HeaderText="Total" ReadOnly="True"
                                SortExpression="Total" />
                        </Fields>
                    </asp:DetailsView>
                    <asp:SqlDataSource ID="SqlDataSource15" runat="server" ConnectionString="<%$ ConnectionStrings:East1DbConnectionString %>"
                        SelectCommand="select (Select   .01*( Sum(Col3)+Sum(col4)+Sum(col5) )/(datediff(second, MIN(COL1), MAX(Col1)) )&#13;&#10;FROM East1DB.dbo.MAINTABLE ) +&#13;&#10;&#13;&#10;(select .01*( Sum(Col3)+Sum(col4)+Sum(col5) )/(datediff(second, MIN(COL1), MAX(Col1)) )&#13;&#10;FROM East2DB.dbo.MAINTABLE ) as Total">
                    </asp:SqlDataSource>
                </td>
                <td style="width: 16px; height: 12px">
                    <asp:DetailsView ID="DetailsView7" runat="server" AutoGenerateRows="False" BackColor="White"
                        BorderColor="White" BorderStyle="Ridge" BorderWidth="2px" CellPadding="3" CellSpacing="1"
                        DataSourceID="SqlDataSource7" GridLines="None" Height="20px" Width="40px">
                        <FooterStyle BackColor="#C6C3C6" ForeColor="Black" />
                        <RowStyle BackColor="#DEDFDE" ForeColor="Black" />
                        <PagerStyle BackColor="#C6C3C6" ForeColor="Black" HorizontalAlign="Right" />
                        <Fields>
                            <asp:BoundField DataField="Column1" DataFormatString="{0:F3} " HeaderText="WEST1"
                                ReadOnly="True" SortExpression="Column1" />
                        </Fields>
                        <HeaderStyle BackColor="#4A3C8C" Font-Bold="True" ForeColor="#E7E7FF" />
                        <EditRowStyle BackColor="#9471DE" Font-Bold="True" ForeColor="White" />
                    </asp:DetailsView>
                    <asp:SqlDataSource ID="SqlDataSource7" runat="server" ConnectionString="<%$ ConnectionStrings:West1DbConnectionString %>"
                        SelectCommand="SELECT  .01*( Sum(Col3)+Sum(col4)+Sum(col5) )/(datediff(second, MIN(COL1), MAX(Col1)) )&#13;&#10;FROM MAINTABLE">
                    </asp:SqlDataSource>
                    <asp:DetailsView ID="DetailsView8" runat="server" AutoGenerateRows="False" BackColor="White"
                        BorderColor="White" BorderStyle="Ridge" BorderWidth="2px" CellPadding="3" CellSpacing="1"
                        DataSourceID="SqlDataSource8" GridLines="None" Height="20px" Width="40px">
                        <FooterStyle BackColor="#C6C3C6" ForeColor="Black" />
                        <RowStyle BackColor="#DEDFDE" ForeColor="Black" />
                        <PagerStyle BackColor="#C6C3C6" ForeColor="Black" HorizontalAlign="Right" />
                        <Fields>
                            <asp:BoundField DataField="Column1" DataFormatString="{0:F3} " HeaderText="WEST2"
                                ReadOnly="True" SortExpression="Column1" />
                        </Fields>
                        <HeaderStyle BackColor="#4A3C8C" Font-Bold="True" ForeColor="#E7E7FF" />
                        <EditRowStyle BackColor="#9471DE" Font-Bold="True" ForeColor="White" />
                    </asp:DetailsView>
                    <asp:SqlDataSource ID="SqlDataSource8" runat="server" ConnectionString="<%$ ConnectionStrings:West2DbConnectionString %>"
                        SelectCommand="SELECT  .01*( Sum(Col3)+Sum(col4))/(datediff(second, MIN(COL1), MAX(Col1)) )&#13;&#10;FROM MAINTABLE">
                    </asp:SqlDataSource>
                    <asp:DetailsView ID="DetailsView9" runat="server" AutoGenerateRows="False" BackColor="White"
                        BorderColor="White" BorderStyle="Ridge" BorderWidth="2px" CellPadding="3" CellSpacing="1"
                        DataSourceID="SqlDataSource9" GridLines="None" Height="20px" Width="40px">
                        <FooterStyle BackColor="#C6C3C6" ForeColor="Black" />
                        <RowStyle BackColor="#DEDFDE" ForeColor="Black" />
                        <PagerStyle BackColor="#C6C3C6" ForeColor="Black" HorizontalAlign="Right" />
                        <Fields>
                            <asp:BoundField DataField="Column1" DataFormatString="{0:F3}" HeaderText="HVAC" ReadOnly="True"
                                SortExpression="Column1" />
                        </Fields>
                        <HeaderStyle BackColor="#4A3C8C" Font-Bold="True" ForeColor="#E7E7FF" />
                        <EditRowStyle BackColor="#9471DE" Font-Bold="True" ForeColor="White" />
                    </asp:DetailsView>
                    <asp:SqlDataSource ID="SqlDataSource9" runat="server" ConnectionString="<%$ ConnectionStrings:East3DbConnectionString %>"
                        SelectCommand="SELECT  .01*( Sum(Col3)+Sum(col4)+Sum(col5) )/(datediff(second, MIN(COL1), MAX(Col1)) )&#13;&#10;FROM MAINTABLE">
                    </asp:SqlDataSource>
                    <asp:DetailsView ID="DetailsView17" runat="server" AutoGenerateRows="False" DataSourceID="SqlDataSource17"
                        Height="22px" Width="125px">
                        <Fields>
                            <asp:BoundField DataField="Total" DataFormatString="{0:F3}" HeaderText="Total" ReadOnly="True"
                                SortExpression="Total" />
                        </Fields>
                    </asp:DetailsView>
                    <asp:SqlDataSource ID="SqlDataSource17" runat="server" ConnectionString="<%$ ConnectionStrings:West1DbConnectionString %>"
                        SelectCommand="select (Select   .01*( Sum(Col3)+Sum(col4)+Sum(col5) )/(datediff(second, MIN(COL1), MAX(Col1)) )&#13;&#10;FROM West1DB.dbo.MAINTABLE ) +&#13;&#10;&#13;&#10;(select .01*( Sum(Col3)+Sum(col4)+Sum(col5) )/(datediff(second, MIN(COL1), MAX(Col1)) )&#13;&#10;FROM West2DB.dbo.MAINTABLE ) +&#13;&#10;&#13;&#10;(select .01*( Sum(Col3)+Sum(col4)+Sum(col5) )/(datediff(second, MIN(COL1), MAX(Col1)) )&#13;&#10;FROM East3DB.dbo.MAINTABLE )&#13;&#10;&#13;&#10;as Total">
                    </asp:SqlDataSource>
                </td>
            </tr>
        </table>

    </div>
    </form>
   </body>
</html>