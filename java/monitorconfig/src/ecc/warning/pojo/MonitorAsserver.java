package ecc.warning.pojo;

import java.sql.ResultSet;
import java.sql.SQLException;

import org.nutz.dao.entity.annotation.Column;
import org.nutz.dao.entity.annotation.Id;
import org.nutz.dao.entity.annotation.Name;
import org.nutz.dao.entity.annotation.Prev;
import org.nutz.dao.entity.annotation.SQL;
import org.nutz.dao.entity.annotation.Table;

@Table("ECC_MONITOR_ASSERVER")
public class MonitorAsserver {
	public MonitorAsserver(){}
	/**
	 * 有加静态的工厂方法，nutz默认会最优先调用，这样不是采用反射机制，效率高.
	 * @param rs
	 * @return
	 * @throws SQLException
	 */
	public static MonitorAsserver getInstance(ResultSet rs) throws SQLException{
		MonitorAsserver ma=new MonitorAsserver();
		ma.url=rs.getString("url");
		ma.seq=rs.getString("seq");
		ma.aboutSystem=rs.getString("about_system");
		ma.scanSts=rs.getString("scan_sts");
		ma.sts=rs.getString("sts");
		ma.areaCode=rs.getString("area_code");
		ma.urlContent=rs.getString("url_content");
		ma.monitorName=rs.getString("monitor_name");
		return ma;
	}
	@Name
	@Prev( @SQL("select max(to_number(seq))+1 from ECC_MONITOR_ASSERVER") )
	@Column
	private String seq;
	@Column("monitor_name")
	private String monitorName;
	@Column
	private String url;
	@Column("about_system")
	private String aboutSystem;
	@Column("scan_sts")
	private String scanSts;
	@Column
	private String sts;
	@Column("area_code")
	private String areaCode;
	@Column("url_content")
	private String urlContent;
	/**
	 * @return the seq
	 */
	public final String getSeq() {
		return seq;
	}
	/**
	 * @param seq the seq to set
	 */
	public final void setSeq(String seq) {
		this.seq = seq;
	}
	/**
	 * @return the monitorName
	 */
	public final String getMonitorName() {
		return monitorName;
	}
	/**
	 * @param monitorName the monitorName to set
	 */
	public final void setMonitorName(String monitorName) {
		this.monitorName = monitorName;
	}
	/**
	 * @return the url
	 */
	public final String getUrl() {
		return url;
	}
	/**
	 * @param url the url to set
	 */
	public final void setUrl(String url) {
		this.url = url;
	}
	/**
	 * @return the aboutSystem
	 */
	public final String getAboutSystem() {
		return aboutSystem;
	}
	/**
	 * @param aboutSystem the aboutSystem to set
	 */
	public final void setAboutSystem(String aboutSystem) {
		this.aboutSystem = aboutSystem;
	}
	/**
	 * @return the scanSts
	 */
	public final String getScanSts() {
		return scanSts;
	}
	/**
	 * @param scanSts the scanSts to set
	 */
	public final void setScanSts(String scanSts) {
		this.scanSts = scanSts;
	}
	/**
	 * @return the sts
	 */
	public final String getSts() {
		return sts;
	}
	/**
	 * @param sts the sts to set
	 */
	public final void setSts(String sts) {
		this.sts = sts;
	}
	/**
	 * @return the areaCode
	 */
	public final String getAreaCode() {
		return areaCode;
	}
	/**
	 * @param areaCode the areaCode to set
	 */
	public final void setAreaCode(String areaCode) {
		this.areaCode = areaCode;
	}
	/**
	 * @return the urlContent
	 */
	public final String getUrlContent() {
		return urlContent;
	}
	/**
	 * @param urlContent the urlContent to set
	 */
	public final void setUrlContent(String urlContent) {
		this.urlContent = urlContent;
	}
	
	
	

}
