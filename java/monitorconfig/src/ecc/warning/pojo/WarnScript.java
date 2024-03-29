package ecc.warning.pojo;

import org.nutz.dao.entity.annotation.Column;
import org.nutz.dao.entity.annotation.Name;
import org.nutz.dao.entity.annotation.Prev;
import org.nutz.dao.entity.annotation.SQL;
import org.nutz.dao.entity.annotation.Table;

@Table("WARN_SCRIPT")
public class WarnScript {
	public WarnScript(){
		
	}
	@Name
	@Prev( @SQL("select nvl(max(to_number(script_id))+1,1) from WARN_SCRIPT") )
	@Column("script_id")
	private String scriptId;
	@Column
	private String sts;
	@Column("remark")
	private String scriptRemark;
	@Column("SCRIPTBASH")
	private String scriptbash;
	/**
	 * @return the scriptId
	 */
	public String getScriptId() {
		return scriptId;
	}
	/**
	 * @param scriptId the scriptId to set
	 */
	public void setScriptId(String scriptId) {
		this.scriptId = scriptId;
	}
	/**
	 * @return the sts
	 */
	public String getSts() {
		return sts;
	}
	/**
	 * @param sts the sts to set
	 */
	public void setSts(String sts) {
		this.sts = sts;
	}
	
	/**
	 * @return the scriptRemark
	 */
	public String getScriptRemark() {
		return scriptRemark;
	}
	/**
	 * @param scriptRemark the scriptRemark to set
	 */
	public void setScriptRemark(String scriptRemark) {
		this.scriptRemark = scriptRemark;
	}
	/**
	 * @return the scriptbash
	 */
	public String getScriptbash() {
		return scriptbash;
	}
	/**
	 * @param scriptbash the scriptbash to set
	 */
	public void setScriptbash(String scriptbash) {
		this.scriptbash = scriptbash;
	}
	

}
